PYODIDE_ROOT=$(abspath ..)
include ../Makefile.envs

all: emsdk/.complete

# We hack the CPU_CORES, because if you use all of the cores on Circle-CI, you
# run out of memory.

emsdk/.complete:
	if [ -d emsdk ]; then rm -rf emsdk; fi
	git clone git@github.com:emscripten-core/emsdk.git	
	( \
		cd emsdk && \
		./emsdk install $(EMSCRIPTEN_SDK) && \
		./emsdk activate $(EMSCRIPTE_SDK) && \
		cd .. && \
		cat extra_libc.imports >> emsdk/upstream/$(EMSCRIPTEN_VERSION)/sysroot/lib/libc.imports && \
    touch .complete \
	)

clean:
	rm -rf emsdk
