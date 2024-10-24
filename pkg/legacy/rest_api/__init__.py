from quart import Quart, request
from quart_cors import cors
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_headers
from pydantic import BaseModel
from sentry_sdk import capture_exception
import time, os

from .v0 import v0


from .admin import admin_bp

from database import db
from sessions import AccSession
import security


# Init app
app = Quart(__name__)
app.config["APPLICATION_ROOT"] = os.getenv("API_ROOT", "")
app.url_map.strict_slashes = False
cors(app, allow_origin="*")
QuartSchema(app)


class TokenHeader(BaseModel):
    token: str | None = None
    username: str | None = None


@app.before_request
async def check_repair_mode():
    if app.supporter.repair_mode and request.path != "/status":
        return {"error": True, "type": "repairModeEnabled"}, 503


@app.before_request
async def get_ip():
    if hasattr(request, "internal_ip") and request.internal_ip:  # internal IP forwarding
        request.ip = request.internal_ip
    else:
        request.ip = (request.headers.get("Cf-Connecting-Ip", request.remote_addr))


@app.before_request
@validate_headers(TokenHeader)
async def check_auth(headers: TokenHeader):
    # Init request user and permissions
    request.user = None
    request.permissions = 0

    # Authenticate request
    account = None
    if request.path != "/status":
        if headers.token:  # external auth
            try:
                username = AccSession.get_username_by_token(headers.token)
            except Exception as e:
                capture_exception(e)
            else:
                account = db.usersv0.find_one({"_id": username}, projection={
                    "_id": 1,
                    "flags": 1,
                    "permissions": 1,
                    "ban.state": 1,
                    "ban.expires": 1
                })
        
        if account:
            if account["ban"]["state"] == "perm_ban" or (account["ban"]["state"] == "temp_ban" and account["ban"]["expires"] > time.time()):
                return {"error": True, "type": "accountBanned"}, 403
            request.user = account["_id"]
            request.flags = account["flags"]
            request.permissions = account["permissions"]


@app.get("/ulist")
async def get_ulist():
    # Get page
    try:
        page = int(request.args["page"])
    except:
        page = 1

    # Get online usernames
    usernames = list(app.cl.usernames.keys())

    # Get total pages
    pages = (len(usernames) // 25)
    if (len(usernames) % 25) > 0:
        pages += 1

    # Truncate list
    usernames = usernames[((page-1)*25):(((page-1)*25)+25)]

    # Return users
    return {
        "error": False,
        "autoget": [security.get_account(username) for username in usernames],
        "page#": page,
        "pages": pages
    }, 200


@app.errorhandler(RequestSchemaValidationError)
async def validation_error(e):
    return {"error": True, "type": "badRequest"}, 400


@app.errorhandler(400)  # Bad request
async def bad_request(e):
    return {"error": True, "type": "badRequest"}, 400


@app.errorhandler(401)  # Unauthorized
async def unauthorized(e):
    return {"error": True, "type": "Unauthorized"}, 401


@app.errorhandler(403)  # Missing permissions
async def missing_permissions(e):
    return {"error": True, "type": "missingPermissions"}, 403


@app.errorhandler(404)  # We do need a 404 handler.
async def not_found(e):
    return {"error": True, "type": "notFound"}, 404


@app.errorhandler(405)  # Method not allowed
async def method_not_allowed(e):
    return {"error": True, "type": "methodNotAllowed"}, 405


@app.errorhandler(429)  # Too many requests
async def too_many_requests(e):
    return {"error": True, "type": "tooManyRequests"}, 429


@app.errorhandler(500)  # Internal
async def internal(e):
    return {"error": True, "type": "Internal"}, 500


@app.errorhandler(501)  # Not implemented
async def not_implemented(e):
      return {"error": True, "type": "notImplemented"}, 501


# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(v0, url_prefix="/v0")
app.register_blueprint(v0, url_prefix="/", name="root")