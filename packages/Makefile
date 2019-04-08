PYODIDE_ROOT=$(abspath ..)
include ../Makefile.envs

all: deps
	../bin/pyodide buildall . ../build --package_abi=$(PYODIDE_PACKAGE_ABI)
deps:
	# Install build dependencies
	$(HOSTPYTHON) -m pip install Cython Tempita pyyaml

clean:
	rm -rf ./*/build
