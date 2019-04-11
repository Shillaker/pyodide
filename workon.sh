#!/bin/bash

# Start with a clean slate (assuming GCC)
CC=cc
AR=ar
CXX=c++
CFLAGS=
CXXFLAGS=
CPP=cpp

# Toolchain
WASM_BIN=/usr/local/code/faasm/pyodide/emsdk/emsdk/upstream/latest/bin
source /usr/local/code/faasm/pyodide/emsdk/emsdk/emsdk_env.sh
echo "PATH += ${WASM_BIN}"
export PATH=${WASM_BIN}:${PATH}

# Make sure Emscripten uses wasm backend (not that it should be invoked)
export EMCC_WASM_BACKEND=1

# Force the use of the required python 3.7 on the host
PYTHON=/usr/local/faasm/python3.7/bin/python3.7
if [ ! -d "venv" ]; then
    ${PYTHON} -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
