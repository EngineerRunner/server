# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61uth_service.proto\x12\x04\x61uth\"\x1e\n\rCheckTokenReq\x12\r\n\x05token\x18\x01 \x01(\t\"0\n\x0e\x43heckTokenResp\x12\r\n\x05valid\x18\x01 \x01(\x08\x12\x0f\n\x07user_id\x18\x02 \x01(\t2?\n\x04\x41uth\x12\x37\n\nCheckToken\x12\x13.auth.CheckTokenReq\x1a\x14.auth.CheckTokenRespB\x04Z\x02./b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\002./'
  _globals['_CHECKTOKENREQ']._serialized_start=28
  _globals['_CHECKTOKENREQ']._serialized_end=58
  _globals['_CHECKTOKENRESP']._serialized_start=60
  _globals['_CHECKTOKENRESP']._serialized_end=108
  _globals['_AUTH']._serialized_start=110
  _globals['_AUTH']._serialized_end=173
# @@protoc_insertion_point(module_scope)