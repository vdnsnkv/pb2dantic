#!/bin/bash

python -m grpc_tools.protoc    \
        -I ./                  \
       --python_out=./         \
       test.proto
