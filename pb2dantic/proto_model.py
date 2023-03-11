from datetime import datetime, timezone

from pydantic import BaseModel
from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict


def _preprocess_data_pb2_single(value):
    if isinstance(value, datetime):
        ts = Timestamp()
        if value.tzinfo is None:
            ts.FromDatetime(value.replace(tzinfo=timezone.utc))
        else:
            ts.FromDatetime(value)
        return ts
    return value


def _preprocess_data_pb2(data):
    if isinstance(data, dict):
        return {k: _preprocess_data_pb2(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_preprocess_data_pb2(v) for v in data]

    return _preprocess_data_pb2_single(data)


class ProtoModel(BaseModel):
    class Config:
        pb2_schema = Message
        allow_population_by_field_name = True

    def pb2(self) -> Message:
        data = self.dict(by_alias=True, exclude_unset=True)
        return self.Config.pb2_schema(**_preprocess_data_pb2(data))

    def serialize(self):
        return self.pb2().SerializeToString()

    @classmethod
    def from_pb2(cls, msg: Message):
        return cls.parse_obj(
            MessageToDict(
                msg,
                preserving_proto_field_name=True,
                use_integers_for_enums=True,
            )
        )

    @classmethod
    def deserialize(cls, data: bytes):
        pb2 = cls.Config.pb2_schema()
        pb2.ParseFromString(data)
        return cls.from_pb2(pb2)
