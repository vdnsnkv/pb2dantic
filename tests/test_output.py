import enum
import typing as t
from datetime import datetime

from pydantic import Field

from pb2dantic import ProtoModel

import tests.test_pb2 as pb2


class ExampleEnum(enum.IntEnum):
    FOO = 0
    BAR = 1
    BUZZ = 2


class SimpleTypesMessage(ProtoModel):
    field_double: float = 0.0
    field_float: float = 0.0
    field_int64: int = 0
    field_uint64: int = 0
    field_int32: int = 0
    field_fixed64: int = 0
    field_fixed32: int = 0
    field_bool: bool = False
    field_string: str = ""
    field_bytes: bytes = b""

    class Config:
        pb2_schema = pb2.SimpleTypesMessage


class NestedMessage(ProtoModel):
    key: str = ""
    value: float = 0.0

    class Config:
        pb2_schema = pb2.NestedMessage


class ComplexTypesMessage(ProtoModel):
    field_string: str = Field("", alias="fieldString")
    optional_int32: int = 0
    repeated_float: t.List[float] = []
    nested: NestedMessage = NestedMessage()
    repeated_nested: t.List[NestedMessage] = []
    optional_nested: NestedMessage = Field(NestedMessage(), alias="optionalNested")
    field_enum: ExampleEnum = Field(ExampleEnum(0), alias="fieldEnum")
    ts: datetime = datetime(1970, 1, 1)

    class Config:
        pb2_schema = pb2.ComplexTypesMessage
