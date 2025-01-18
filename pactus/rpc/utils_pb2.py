# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0butils.proto\x12\x06pactus\"]\n SignMessageWithPrivateKeyRequest\x12\x1f\n\x0bprivate_key\x18\x01 \x01(\tR\nprivateKey\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\"A\n!SignMessageWithPrivateKeyResponse\x12\x1c\n\tsignature\x18\x01 \x01(\tR\tsignature\"m\n\x14VerifyMessageRequest\x12\x18\n\x07message\x18\x01 \x01(\tR\x07message\x12\x1c\n\tsignature\x18\x02 \x01(\tR\tsignature\x12\x1d\n\npublic_key\x18\x03 \x01(\tR\tpublicKey\"2\n\x15VerifyMessageResponse\x12\x19\n\x08is_valid\x18\x01 \x01(\x08R\x07isValid\"A\n\x1e\x42LSPublicKeyAggregationRequest\x12\x1f\n\x0bpublic_keys\x18\x01 \x03(\tR\npublicKeys\"Z\n\x1f\x42LSPublicKeyAggregationResponse\x12\x1d\n\npublic_key\x18\x01 \x01(\tR\tpublicKey\x12\x18\n\x07\x61\x64\x64ress\x18\x02 \x01(\tR\x07\x61\x64\x64ress\"@\n\x1e\x42LSSignatureAggregationRequest\x12\x1e\n\nsignatures\x18\x01 \x03(\tR\nsignatures\"?\n\x1f\x42LSSignatureAggregationResponse\x12\x1c\n\tsignature\x18\x01 \x01(\tR\tsignature2\x9f\x03\n\x05Utils\x12p\n\x19SignMessageWithPrivateKey\x12(.pactus.SignMessageWithPrivateKeyRequest\x1a).pactus.SignMessageWithPrivateKeyResponse\x12L\n\rVerifyMessage\x12\x1c.pactus.VerifyMessageRequest\x1a\x1d.pactus.VerifyMessageResponse\x12j\n\x17\x42LSPublicKeyAggregation\x12&.pactus.BLSPublicKeyAggregationRequest\x1a\'.pactus.BLSPublicKeyAggregationResponse\x12j\n\x17\x42LSSignatureAggregation\x12&.pactus.BLSSignatureAggregationRequest\x1a\'.pactus.BLSSignatureAggregationResponseB@\n\x0cpactus.utilsZ0github.com/pactus-project/pactus/www/grpc/pactusb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\014pactus.utilsZ0github.com/pactus-project/pactus/www/grpc/pactus'
  _SIGNMESSAGEWITHPRIVATEKEYREQUEST._serialized_start=23
  _SIGNMESSAGEWITHPRIVATEKEYREQUEST._serialized_end=116
  _SIGNMESSAGEWITHPRIVATEKEYRESPONSE._serialized_start=118
  _SIGNMESSAGEWITHPRIVATEKEYRESPONSE._serialized_end=183
  _VERIFYMESSAGEREQUEST._serialized_start=185
  _VERIFYMESSAGEREQUEST._serialized_end=294
  _VERIFYMESSAGERESPONSE._serialized_start=296
  _VERIFYMESSAGERESPONSE._serialized_end=346
  _BLSPUBLICKEYAGGREGATIONREQUEST._serialized_start=348
  _BLSPUBLICKEYAGGREGATIONREQUEST._serialized_end=413
  _BLSPUBLICKEYAGGREGATIONRESPONSE._serialized_start=415
  _BLSPUBLICKEYAGGREGATIONRESPONSE._serialized_end=505
  _BLSSIGNATUREAGGREGATIONREQUEST._serialized_start=507
  _BLSSIGNATUREAGGREGATIONREQUEST._serialized_end=571
  _BLSSIGNATUREAGGREGATIONRESPONSE._serialized_start=573
  _BLSSIGNATUREAGGREGATIONRESPONSE._serialized_end=636
  _UTILS._serialized_start=639
  _UTILS._serialized_end=1054
# @@protoc_insertion_point(module_scope)
