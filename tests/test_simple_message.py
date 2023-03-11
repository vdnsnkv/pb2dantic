from .test_output import SimpleTypesMessage

from tests.test_utils import assert_messages_equal, test_pb2 as pb2

SERIALIZED_MESSAGE_EMPTY = b""
SERIALIZED_MESSAGE_WITH_DATA = b"\t\x00\x00\x00\x00\x00\x00\xf0?\x15\x00\x00\x00@\x18\x03 \x04(\x051\x06\x00\x00\x00\x00\x00\x00\x00=\x07\x00\x00\x00@\x01J\x0bTEST_STRING"


def test_create_empty_model():
    pydantic_model = SimpleTypesMessage()

    assert pydantic_model.field_double == 0.0
    assert pydantic_model.field_float == 0.0
    assert pydantic_model.field_int64 == 0
    assert pydantic_model.field_uint64 == 0
    assert pydantic_model.field_int32 == 0
    assert pydantic_model.field_fixed64 == 0
    assert pydantic_model.field_fixed32 == 0
    assert pydantic_model.field_bool is False
    assert pydantic_model.field_string == ""


def test_empty_model_pb2():
    pydantic_model = SimpleTypesMessage()

    pb2_message = pb2.SimpleTypesMessage()

    assert_messages_equal(pydantic_model.pb2(), pb2_message)


def test_empty_model_serialize():
    pydantic_model = SimpleTypesMessage()

    assert pydantic_model.serialize() == SERIALIZED_MESSAGE_EMPTY


def test_empty_model_deserialize():
    pydantic_model = SimpleTypesMessage.deserialize(SERIALIZED_MESSAGE_EMPTY)

    assert pydantic_model.field_double == 0.0
    assert pydantic_model.field_float == 0.0
    assert pydantic_model.field_int64 == 0
    assert pydantic_model.field_uint64 == 0
    assert pydantic_model.field_int32 == 0
    assert pydantic_model.field_fixed64 == 0
    assert pydantic_model.field_fixed32 == 0
    assert pydantic_model.field_bool is False
    assert pydantic_model.field_string == ""


DATA = {
    "field_double": 1.0,
    "field_float": 2.0,
    "field_int64": 3,
    "field_uint64": 4,
    "field_int32": 5,
    "field_fixed64": 6,
    "field_fixed32": 7,
    "field_bool": True,
    "field_string": "TEST_STRING",
}


def test_create_model():
    pydantic_model = SimpleTypesMessage(**DATA)

    assert pydantic_model.field_double == 1.0
    assert pydantic_model.field_float == 2.0
    assert pydantic_model.field_int64 == 3
    assert pydantic_model.field_uint64 == 4
    assert pydantic_model.field_int32 == 5
    assert pydantic_model.field_fixed64 == 6
    assert pydantic_model.field_fixed32 == 7
    assert pydantic_model.field_bool is True
    assert pydantic_model.field_string == "TEST_STRING"


def test_model_pb2():
    pydantic_model = SimpleTypesMessage(**DATA)

    pb2_message = pb2.SimpleTypesMessage(**DATA)

    assert_messages_equal(pydantic_model.pb2(), pb2_message)


def test_model_deserialize():
    pydantic_model = SimpleTypesMessage.deserialize(SERIALIZED_MESSAGE_WITH_DATA)

    assert pydantic_model.field_double == 1.0
    assert pydantic_model.field_float == 2.0
    assert pydantic_model.field_int64 == 3
    assert pydantic_model.field_uint64 == 4
    assert pydantic_model.field_int32 == 5
    assert pydantic_model.field_fixed64 == 6
    assert pydantic_model.field_fixed32 == 7
    assert pydantic_model.field_bool is True
    assert pydantic_model.field_string == "TEST_STRING"