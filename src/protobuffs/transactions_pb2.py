# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transactions.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12transactions.proto\x12\x05proto\"\xf2\x04\n\x05Stock\x12#\n\x06symbol\x18\x01 \x01(\x0e\x32\x13.proto.Stock.Symbol\x12\r\n\x05price\x18\x02 \x01(\x02\x12\x0b\n\x03qty\x18\x03 \x01(\x02\"\xa7\x04\n\x06Symbol\x12\n\n\x06TWILIO\x10\x00\x12\t\n\x05\x41PPLE\x10\x01\x12\n\n\x06\x41MAZON\x10\x02\x12\n\n\x06GOOGLE\x10\x03\x12\r\n\tMICROSOFT\x10\x04\x12\x0c\n\x08\x42\x41RCLAYS\x10\x05\x12\x07\n\x03IBM\x10\x06\x12\x0b\n\x07METLIFE\x10\x07\x12\x0b\n\x07PHILIPS\x10\x08\x12\x11\n\rPHILIP_MORRIS\x10\t\x12\x07\n\x03UPS\x10\n\x12\x07\n\x03\x41MD\x10\x0b\x12\r\n\tHONEYWELL\x10\x0c\x12\x0e\n\nMASTERCARD\x10\r\x12\x07\n\x03MSI\x10\x0e\x12\n\n\x06NVIDIA\x10\x0f\x12\x10\n\x0cPURE_STORAGE\x10\x10\x12\x10\n\x0cSENTINEL_ONE\x10\x11\x12\n\n\x06SPLUNK\x10\x12\x12\x08\n\x04VISA\x10\x13\x12\x0f\n\x0b\x43\x41TERPILLAR\x10\x14\x12\x0b\n\x07\x43OLGATE\x10\x15\x12\t\n\x05\x46\x45\x44\x45X\x10\x16\x12\x14\n\x10GENERAL_ELECTRIC\x10\x17\x12\x0b\n\x07JOHNSON\x10\x18\x12\x08\n\x04MERK\x10\x19\x12\t\n\x05PEPSI\x10\x1a\x12\x16\n\x12PROCTOR_AND_GAMBLE\x10\x1b\x12\r\n\tSTARBUCKS\x10\x1c\x12\n\n\x06SCHWAB\x10\x1d\x12\t\n\x05SHELL\x10\x1e\x12\x06\n\x02\x42P\x10\x1f\x12\x17\n\x13PETROLEO_BRASILEIRO\x10 \x12\x0e\n\nVOLKSWAGEN\x10!\x12\t\n\x05\x43ISCO\x10\"\x12\x0f\n\x0b\x41STRA_SPACE\x10#\x12\x19\n\x15VIRGIN_GALACTIC_SPACE\x10$\x12\x14\n\x07UNKNOWN\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\"+\n\x0cTransactions\x12\x1b\n\x05stock\x18\x01 \x03(\x0b\x32\x0c.proto.Stockb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transactions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_STOCK']._serialized_start=30
  _globals['_STOCK']._serialized_end=656
  _globals['_STOCK_SYMBOL']._serialized_start=105
  _globals['_STOCK_SYMBOL']._serialized_end=656
  _globals['_TRANSACTIONS']._serialized_start=658
  _globals['_TRANSACTIONS']._serialized_end=701
# @@protoc_insertion_point(module_scope)
