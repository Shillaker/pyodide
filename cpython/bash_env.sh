#!/bin/bash

export EMCC_WASM_BACKEND=1

PYTHON=/usr/local/faasm/python3.7/bin/python3.7

if [ ! -d "venv" ]; then
    ${PYTHON} -m venv venv
fi

source venv/bin/activate
