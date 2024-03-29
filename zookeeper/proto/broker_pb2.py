# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: broker.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62roker.proto\"+\n\rBrokerMessage\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"D\n\x12\x42rokerPushResponse\x12\x1d\n\x06status\x18\x01 \x01(\x0e\x32\r.BrokerStatus\x12\x0f\n\x07message\x18\x02 \x01(\t\"T\n\x12\x42rokerPullResponse\x12\x1d\n\x06status\x18\x01 \x01(\x0e\x32\r.BrokerStatus\x12\x1f\n\x07message\x18\x02 \x01(\x0b\x32\x0e.BrokerMessage\"+\n\x0eReplicaRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\"0\n\x0fReplicaResponse\x12\x1d\n\x06status\x18\x01 \x01(\x0e\x32\r.BrokerStatus\"/\n\x0bMessageList\x12 \n\x08messages\x18\x01 \x03(\x0b\x32\x0e.BrokerMessage\"\x1d\n\x0cMessageCount\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\"\r\n\x0b\x42rokerEmpty*6\n\x0c\x42rokerStatus\x12\x12\n\x0e\x42ROKER_SUCCESS\x10\x00\x12\x12\n\x0e\x42ROKER_FAILURE\x10\x01\x32\x80\x03\n\x06\x42roker\x12#\n\x03\x41\x63k\x12\x0c.BrokerEmpty\x1a\x0c.BrokerEmpty\"\x00\x12-\n\x04Push\x12\x0e.BrokerMessage\x1a\x13.BrokerPushResponse\"\x00\x12+\n\x04Pull\x12\x0c.BrokerEmpty\x1a\x13.BrokerPullResponse\"\x00\x12\x31\n\nSetReplica\x12\x0f.ReplicaRequest\x1a\x10.ReplicaResponse\"\x00\x12+\n\x0bLeadReplica\x12\x0c.BrokerEmpty\x1a\x0c.BrokerEmpty\"\x00\x12+\n\x0b\x44ropReplica\x12\x0c.BrokerEmpty\x1a\x0c.BrokerEmpty\"\x00\x12\x32\n\x0bPushReplica\x12\x0c.MessageList\x1a\x13.BrokerPushResponse\"\x00\x12\x34\n\x13\x44ropReplicaMessages\x12\r.MessageCount\x1a\x0c.BrokerEmpty\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'broker_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BROKERSTATUS']._serialized_start=407
  _globals['_BROKERSTATUS']._serialized_end=461
  _globals['_BROKERMESSAGE']._serialized_start=16
  _globals['_BROKERMESSAGE']._serialized_end=59
  _globals['_BROKERPUSHRESPONSE']._serialized_start=61
  _globals['_BROKERPUSHRESPONSE']._serialized_end=129
  _globals['_BROKERPULLRESPONSE']._serialized_start=131
  _globals['_BROKERPULLRESPONSE']._serialized_end=215
  _globals['_REPLICAREQUEST']._serialized_start=217
  _globals['_REPLICAREQUEST']._serialized_end=260
  _globals['_REPLICARESPONSE']._serialized_start=262
  _globals['_REPLICARESPONSE']._serialized_end=310
  _globals['_MESSAGELIST']._serialized_start=312
  _globals['_MESSAGELIST']._serialized_end=359
  _globals['_MESSAGECOUNT']._serialized_start=361
  _globals['_MESSAGECOUNT']._serialized_end=390
  _globals['_BROKEREMPTY']._serialized_start=392
  _globals['_BROKEREMPTY']._serialized_end=405
  _globals['_BROKER']._serialized_start=464
  _globals['_BROKER']._serialized_end=848
# @@protoc_insertion_point(module_scope)
