from google.protobuf.descriptor import Descriptor, EnumDescriptor

from .str_utils import snake_case
from .field import field_type_definition

DEFAULT_IDENT = " " * 4


def class_name_message(md: Descriptor):
    return f"class {md.name}(ProtoModel):"


def pydantic_model_message(md: Descriptor, ident: str = DEFAULT_IDENT):
    result = class_name_message(md)
    result += "\n"
    for field_name, fd in md.fields_by_name.items():
        result += f"{ident}{snake_case(field_name)}: {field_type_definition(fd)}\n"
    result += "\n"
    result += f"{ident}class Config:"
    result += "\n"
    result += f"{ident}{ident}pb2_schema = pb2.{md.name}"
    return result


def class_name_enum(ed: EnumDescriptor):
    return f"class {ed.name}(enum.IntEnum):"


def pydantic_model_enum(ed: EnumDescriptor, ident: str = DEFAULT_IDENT):
    result = class_name_enum(ed)
    result += "\n"
    for value_name, vd in ed.values_by_name.items():
        result += f"{ident}{value_name} = {vd.number}\n"
    return result
