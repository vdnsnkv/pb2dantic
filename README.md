# pb2dantic

pydantic models for pb2 types

### Generate pydantic models from pb2

Suppose you have a protobuf message definition in `my_message.proto` file

```protobuf
// my_message.proto
syntax = "proto3";

message MyMessage {
  string key = 1;
  float value = 2;
}
```

You can use pb2dantic to get a pydantic model for MyMessage.

First, generate pb2 file from proto
```shell
python -m grpc_tools.protoc -I ./ --python_out=./ my_message.proto
```

Then run pb2dantic

```shell
python -m pb2dantic.generate ./my_message_pb2.py
```

This will generate `my_message_output.py` file with pydantic models

```python
# my_message_output.py

import enum
import typing as t
from datetime import datetime
from pydantic import Field

import my_message_pb2 as pb2
from pb2dantic import ProtoModel


class MyMessage(ProtoModel):
    key: t.Optional[str]
    value: t.Optional[float]

    class Config:
        pb2_schema = pb2.MyMessage
```

Generated models are inherited from ProtoModel class.

Features:

- scalar field types converted to python types according to [proto3 reference](https://developers.google.com/protocol-buffers/docs/proto3#scalar)
- repeated fields support
- nested types support
- enums support
- Timestamp fields are converted to datetime fields
- python objects serialization to binary format according to `pb2_schema` specified in Config
- binary data deserialization to python objects 
- getting pb2 messages from python objects with `.pb2()` method
- creating python objects from pb2 messages

Some examples using MyMessage model from above: 

```python
from my_message_output import MyMessage

msg = MyMessage(key='a', value=1)

print(msg.serialize())
#  b'\n\x01a\x15\x00\x00\x80?'

MyMessage.deserialize(b'\n\x01a\x15\x00\x00\x80?')
# MyMessage(key='a', value=1.0)

msg_pb2 = msg.pb2()

print(msg_pb2)
# key: "a"
# value: 1

MyMessage.from_pb2(msg_pb2)
# MyMessage(key='a', value=1.0)
```
