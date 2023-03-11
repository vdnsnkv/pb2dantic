### TODO

Pydantic models generation from pb2
  - [x] Scalar fields
    - [ ] bytes fields
  - [x] Enums
  - [x] Nested messages
  - [x] Repeated message fields
  - [ ] Maps
  - [ ] Maps of messages
  - [ ] OneOf
  - [ ] Any
  - [x] Google Timestamp
  - [ ] Other Well-known types
  - [ ] Imports in proto files
  - [x] Renaming camel case fields to snake case in models
  - [x] Field types have the same defaults as pb2 messages
  - [ ] Resolve cases when field names clash with language keywords
  
Protobuf base model class
  - [x] Easy model instance creation from pb2 message
    - (without any additional data transformations)
  - [x] Easy pb2 message creation from model 
  - [x] Serialization
    - [x] Don't encode zero values for nested types
    - [x] datetime -> Timestamp serialization
    - [ ] Other Well-known types
    - [ ] Maps
    - [ ] Any
  - [x] Deserialization
    - [x] Timestamp -> datetime deserialization
    - [ ] bytes field deserialization
    - [ ] Other Well-known types
    - [ ] Maps
    - [ ] Any
