EMSCRIPTEN_VERSION=5465
EMSCRIPTEN_SDK=sdk-upstream-$(EMSCRIPTEN_VERSION)-64bit

PYODIDE_ROOT=$(abspath ..)
include ../Makefile.envs

all: emsdk/.built

emsdk/.built:
	if [ -d emsdk ]; then rm -rf emsdk; fi
	git clone git@github.com:emscripten-core/emsdk.git
	cd emsdk &&	./emsdk install $(EMSCRIPTEN_SDK)
	cd emsdk &&	./emsdk activate $(EMSCRIPTEN_SDK)
	cd emsdk/upstream && ln -s $(EMSCRIPTEN_VERSION) latest
	rm -r emsdk/zips
	rm -r emsdk/upstream/latest/fastcomp
	rm -r emsdk/upstream/latest/emscripten
	touch emsdk/.built

clean:
	rm -rf emsdk
