PYODIDE_ROOT=$(abspath ..)
include ../Makefile.envs

all: emsdk/.patched

emsdk/.patched: emsdk/.built
	(cat patches/*.patch | patch -p1);
	touch emsdk/.patched

emsdk/.built:
	if [ -d emsdk ]; then rm -rf emsdk; fi
	git clone git@github.com:emscripten-core/emsdk.git
	cd emsdk &&	./emsdk install $(EMSCRIPTEN_SDK)
	cd emsdk &&	./emsdk activate $(EMSCRIPTEN_SDK) 
	touch emsdk/.built

clean:
	rm -rf emsdk
