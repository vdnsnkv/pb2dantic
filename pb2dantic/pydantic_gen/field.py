from google.protobuf.descriptor import FieldDescriptor

from .str_utils import is_camel_case, snake_case

# https://developers.google.com/protocol-buffers/docs/proto3#scalar
SCALAR_TYPE_MAPPING = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
}
SCALAR_TYPE_DEFAULT_VALUES = {
    FieldDescriptor.TYPE_DOUBLE: 0.0,
    FieldDescriptor.TYPE_FLOAT: 0.0,
    FieldDescriptor.TYPE_INT64: 0,
    FieldDescriptor.TYPE_UINT64: 0,
    FieldDescriptor.TYPE_INT32: 0,
    FieldDescriptor.TYPE_FIXED64: 0,
    FieldDescriptor.TYPE_FIXED32: 0,
    FieldDescriptor.TYPE_BOOL: False,
    FieldDescriptor.TYPE_STRING: "",
    FieldDescriptor.TYPE_BYTES: b"",
    FieldDescriptor.TYPE_UINT32: 0,
    FieldDescriptor.TYPE_SFIXED32: 0,
    FieldDescriptor.TYPE_SFIXED64: 0,
    FieldDescriptor.TYPE_SINT32: 0,
    FieldDescriptor.TYPE_SINT64: 0,
}
REPEATED_FIELD_DEFAULT_VALUE = []

# https://developers.google.com/protocol-buffers/docs/reference/google.protobuf
WELL_KNOWN_TYPES_MAPPING = {
    "Timestamp": "datetime",
}
WELL_KNOWN_TYPES_DEFAULT_VALUES = {
    "Timestamp": "datetime(1970, 1, 1)",
}


def _is_scalar_type(fd: FieldDescriptor):
    return fd.type in SCALAR_TYPE_MAPPING


def _pydantic_field_element_type(fd: FieldDescriptor):
    if _is_scalar_type(fd):
        return SCALAR_TYPE_MAPPING[fd.type].__name__

    elif fd.type == FieldDescriptor.TYPE_MESSAGE:
        field_type = fd.message_type.name
        return WELL_KNOWN_TYPES_MAPPING.get(field_type, field_type)

    elif fd.type == FieldDescriptor.TYPE_ENUM:
        return fd.enum_type.name

    else:
        raise ValueError(f"Unknown field element type for {fd}")


def _pydantic_field_default_value(fd: FieldDescriptor):
    if _has_label_repeated(fd):
        return repr(REPEATED_FIELD_DEFAULT_VALUE)

    elif _is_scalar_type(fd):
        return repr(SCALAR_TYPE_DEFAULT_VALUES[fd.type])

    elif fd.type == FieldDescriptor.TYPE_MESSAGE:
        field_type = fd.message_type.name
        return WELL_KNOWN_TYPES_DEFAULT_VALUES.get(field_type, f"{field_type}()")

    elif fd.type == FieldDescriptor.TYPE_ENUM:
        return f"{fd.enum_type.name}(0)"

    else:
        raise ValueError(f"No default value for {fd}")


def _has_label_repeated(fd: FieldDescriptor):
    return fd.label == FieldDescriptor.LABEL_REPEATED


def _needs_alias(fd: FieldDescriptor):
    return is_camel_case(fd.name)


def _field_alias(fd: FieldDescriptor):
    return fd.name


def _needs_field_function(fd: FieldDescriptor):
    return _needs_alias(fd)


def _field_type(fd: FieldDescriptor):
    element_type = _pydantic_field_element_type(fd)

    if _has_label_repeated(fd):
        return f"t.List[{element_type}]"

    return element_type


def _field_type_description(fd: FieldDescriptor):
    default_value = _pydantic_field_default_value(fd)

    if _needs_field_function(fd):
        return f'Field({default_value}, alias="{_field_alias(fd)}")'

    return default_value


def field_definition(field_name: str, fd: FieldDescriptor):
    return (
        f"{snake_case(field_name)}: {_field_type(fd)} = {_field_type_description(fd)}"
    )
