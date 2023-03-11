from google.protobuf.descriptor import FileDescriptor

from .model import pydantic_model_enum, pydantic_model_message

MODULE_IMPORTS = [
    "import enum",
    "import typing as t",
    "from datetime import datetime",
    "",
    "from pydantic import Field",
    "",
    "from pb2dantic import ProtoModel",
    "",
]


def pydantic_module(pb2_file_descriptor: FileDescriptor, pb2_module_file_name: str):
    pb2_module_import = f"import {pb2_module_file_name.replace('.py', '')} as pb2"
    imports = "\n".join([*MODULE_IMPORTS, pb2_module_import])

    enum_definitions = []
    for _, enum_descriptor in pb2_file_descriptor.enum_types_by_name.items():
        enum_definitions.append(pydantic_model_enum(enum_descriptor))

    class_definitions = []
    for _, msg_desciptor in pb2_file_descriptor.message_types_by_name.items():
        class_definitions.append(pydantic_model_message(msg_desciptor))

    enum_definitions = "\n\n\n".join(enum_definitions)
    class_definitions = "\n\n\n".join(class_definitions)

    return f"{imports}\n\n\n{enum_definitions}\n\n{class_definitions}\n"
