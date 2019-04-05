#!/bin/bash

source /usr/local/code/faasm/pyodide/emsdk/emsdk/emsdk_env.sh
export EMCC_WASM_BACKEND=1

PYTHON=/usr/local/faasm/python3.7/bin/python3.7

if [ ! -d "venv" ]; then
    ${PYTHON} -m venv venv
fi

source venv/bin/activate
