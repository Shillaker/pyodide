PYODIDE_ROOT=$(abspath ..)
PROJ_ROOT=$(PYODIDE_ROOT)/../..
include ../Makefile.envs
include $(PROJ_ROOT)/third-party/faasm-toolchain/Makefile.envs

all: deps
	../bin/pyodide buildall . ../build --package_abi=$(PYODIDE_PACKAGE_ABI)
deps:
	# Install build dependencies
	$(HOSTPYTHON) -m pip install Cython Tempita pyyaml

clean:
	rm -rf ./*/build
