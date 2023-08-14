### TODO

Pydantic models generation from pb2
  - [x] Scalar fields
  - [x] Enums
  - [x] Nested messages
  - [x] Repeated message fields
  - [ ] Maps
  - [ ] Maps of messages
  - [ ] OneOf
  - [ ] Any
  - [x] Google Timestamp
  - [x] Renaming camel case fields to snake case in models
  - [x] Field types have the same defaults as pb2 messages
  - [ ] Resolve cases when field names clash with language keywords
  - [ ] Other Well-known types
    - [ ] Duration
    - [ ] Empty
  - [ ] Imports in proto files
  
Protobuf base model class
  - [x] One-step model instance creation from pb2 message
    - (without any additional data transformations)
  - [x] One-step pb2 message creation from model 
  - [x] Serialization
    - [x] Don't encode zero values for nested types
    - [x] datetime -> Timestamp serialization
    - [x] bytes field serialization
    - [ ] Maps
    - [ ] Any
    - [ ] OneOf
    - [ ] Other Well-known types
  - [x] Deserialization
    - [x] Timestamp -> datetime deserialization
    - [x] bytes field deserialization
    - [ ] Maps
    - [ ] Any
    - [ ] OneOf
    - [ ] Other Well-known types
