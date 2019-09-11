#!/bin/bash

# Toolchain
TOOLCHAIN_ROOT=/usr/local/code/faasm/toolchain
TOOLCHAIN_BIN=${TOOLCHAIN_ROOT}/install/bin
source ${TOOLCHAIN_ROOT}/env.sh

export PATH=${TOOLCHAIN_BIN}:$PATH

# Start with a clean slate (assuming GCC)
CC=${WASM_CC}
AR=${WASM_AR}
CXX=${WASM_CXX}
CFLAGS=${WASM_CFLAGS}
CXXFLAGS=${WASM_CXXFLAGS}
CPP=${WASM_CPP}
RANLIB=${WASM_RANLIB}
LD=${WASM_LD}

echo "New path: ${PATH}"

# Force the use of the required python 3.7 on the host
PYTHON=/usr/local/faasm/python3.7/bin/python3.7
if [ ! -d "venv" ]; then
    ${PYTHON} -m venv venv
fi

export VIRTUAL_ENV_DISABLE_PROMPT=1
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt

export PS1="(pyodide) $PS1"

