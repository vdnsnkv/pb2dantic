from datetime import datetime, timezone

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

import tests.test_pb2 as pb2

from tests.test_output import ComplexTypesMessage, NestedMessage, ExampleEnum
from tests.test_utils import assert_messages_equal

SERIALIZED_MESSAGE_EMPTY = b""
SERIALIZED_MESSAGE_WITH_DATA = b'\n\x0bTEST_STRING\x10\x0c\x1a\x08\x9a\x99\x99?\x9a\x99Y@"\x08\n\x01a\x15\x00\x00\x80?*\x08\n\x01b\x15\x00\x00\x00@*\x08\n\x01c\x15\x00\x00@@8\x01B\x0c\x08\xff\x8f\xad\x9b\x06\x10\xf0\x8a\xba\xbe\x02'

TEST_DT = datetime(2022, 11, 9, 6, 26, 7, 667846)
TEST_TS_PB2 = Timestamp()
TEST_TS_PB2.FromDatetime(TEST_DT)


@pytest.fixture()
def empty_model():
    return ComplexTypesMessage()


def test_create_empty_model(empty_model):
    assert empty_model.field_string == ""
    assert empty_model.optional_int32 == 0
    assert empty_model.repeated_float == []
    assert empty_model.repeated_nested == []

    assert isinstance(empty_model.nested, NestedMessage)
    assert empty_model.nested.key == ""
    assert empty_model.nested.value == 0.0

    assert isinstance(empty_model.optional_nested, NestedMessage)
    assert empty_model.optional_nested.key == ""
    assert empty_model.optional_nested.value == 0.0

    assert isinstance(empty_model.field_enum, ExampleEnum)
    assert empty_model.field_enum.value == ExampleEnum.FOO
    assert empty_model.ts == datetime(1970, 1, 1)


def test_empty_model_pb2(empty_model):
    pb2_message = pb2.ComplexTypesMessage()

    assert_messages_equal(empty_model.pb2(), pb2_message)


def test_empty_model_serialize(empty_model):
    assert empty_model.serialize() == SERIALIZED_MESSAGE_EMPTY


def test_empty_model_deserialize():
    deserialized_model = ComplexTypesMessage.deserialize(SERIALIZED_MESSAGE_EMPTY)

    assert deserialized_model.field_string == ""
    assert deserialized_model.optional_int32 == 0
    assert deserialized_model.repeated_float == []
    assert deserialized_model.repeated_nested == []

    assert isinstance(deserialized_model.nested, NestedMessage)
    assert deserialized_model.nested.key == ""
    assert deserialized_model.nested.value == 0.0

    assert isinstance(deserialized_model.optional_nested, NestedMessage)
    assert deserialized_model.optional_nested.key == ""
    assert deserialized_model.optional_nested.value == 0.0

    assert isinstance(deserialized_model.field_enum, ExampleEnum)
    assert deserialized_model.field_enum.value == ExampleEnum.FOO
    assert deserialized_model.ts == datetime(1970, 1, 1)


DATA = {
    "field_string": "TEST_STRING",
    "optional_int32": 12,
    "repeated_float": [1.2, 3.4],
    "nested": NestedMessage(key="a", value=1),
    "repeated_nested": [
        NestedMessage(key="b", value=2),
        NestedMessage(key="c", value=3),
    ],
    "field_enum": ExampleEnum.BAR,
    "ts": TEST_DT,
}
PB2_DATA = {
    "fieldString": "TEST_STRING",
    "optional_int32": 12,
    "repeated_float": [1.2, 3.4],
    "nested": pb2.NestedMessage(key="a", value=1),
    "repeated_nested": [
        pb2.NestedMessage(key="b", value=2),
        pb2.NestedMessage(key="c", value=3),
    ],
    "fieldEnum": 1,
    "ts": TEST_TS_PB2,
}


def test_create_model():
    pydantic_model = ComplexTypesMessage(**DATA)

    assert pydantic_model.field_string == "TEST_STRING"
    assert pydantic_model.optional_int32 == 12
    assert pydantic_model.repeated_float == [1.2, 3.4]

    assert isinstance(pydantic_model.nested, NestedMessage)
    assert pydantic_model.nested.key == "a"
    assert pydantic_model.nested.value == 1

    assert isinstance(pydantic_model.repeated_nested, list)
    assert isinstance(pydantic_model.repeated_nested[1], NestedMessage)
    assert pydantic_model.repeated_nested[1].key == "c"
    assert pydantic_model.repeated_nested[1].value == 3

    assert isinstance(pydantic_model.optional_nested, NestedMessage)
    assert pydantic_model.optional_nested.key == ""
    assert pydantic_model.optional_nested.value == 0.0

    assert pydantic_model.field_enum == ExampleEnum.BAR
    assert pydantic_model.ts == TEST_DT


def test_model_pb2():
    pydantic_model = ComplexTypesMessage(**DATA)

    pb2_message = pb2.ComplexTypesMessage(**PB2_DATA)

    assert_messages_equal(pydantic_model.pb2(), pb2_message)


def test_model_deserialize():
    pydantic_model = ComplexTypesMessage.deserialize(SERIALIZED_MESSAGE_WITH_DATA)

    assert pydantic_model.field_string == "TEST_STRING"
    assert pydantic_model.optional_int32 == 12
    assert pydantic_model.repeated_float == [1.2, 3.4]

    assert isinstance(pydantic_model.nested, NestedMessage)
    assert pydantic_model.nested.key == "a"
    assert pydantic_model.nested.value == 1

    assert isinstance(pydantic_model.repeated_nested, list)
    assert isinstance(pydantic_model.repeated_nested[1], NestedMessage)
    assert pydantic_model.repeated_nested[1].key == "c"
    assert pydantic_model.repeated_nested[1].value == 3

    assert isinstance(pydantic_model.optional_nested, NestedMessage)
    assert pydantic_model.optional_nested.key == ""
    assert pydantic_model.optional_nested.value == 0.0

    assert pydantic_model.field_enum == ExampleEnum.BAR
    assert pydantic_model.ts == TEST_DT.replace(tzinfo=timezone.utc)
