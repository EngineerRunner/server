from quart import Blueprint, abort
import os, json


emojis_bp = Blueprint("emojis_bp", __name__, url_prefix="/emojis")


DEFAULT_EMOJIS = {}  # {lang: [...]}
for filename in os.listdir("pkg/legacy/emojis"):
    if filename.endswith(".json"):
        f = open(f"pkg/legacy/emojis/{filename}", "r")
        DEFAULT_EMOJIS[filename.replace(".json", "")] = json.load(f)
        f.close()


@emojis_bp.get("/<lang>")
async def get_default_emojis(lang: str):
    if lang in DEFAULT_EMOJIS:
        return {"error": False, "groups": DEFAULT_EMOJIS[lang]}, 200
    else:
        abort(404)
