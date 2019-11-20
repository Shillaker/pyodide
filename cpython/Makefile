PYODIDE_ROOT=$(abspath ..)
PROJ_ROOT=$(PYODIDE_ROOT)/../..
include ../Makefile.envs
include $(PROJ_ROOT)/toolchain/Makefile.envs

ROOT=$(abspath .)

HOSTINSTALL=$(ROOT)/build/$(PYVERSION)/host
HOSTBUILD=$(HOSTINSTALL)/Python-$(PYVERSION)
HOSTPYTHON=$(HOSTINSTALL)/bin/python3$(EXE)
HOSTPGEN=$(HOSTINSTALL)/bin/pgen$(EXE)

# Note: ABIFLAGS differs depending on the type of build you're running. For debug it'll 
# be "d" and using pymalloc it'll be "m". If not using pymalloc it'll be empty.
ABIFLAGS=m
BUILD=$(ROOT)/build/$(PYVERSION)/Python-$(PYVERSION)
INSTALL=$(ROOT)/installs/python-$(PYVERSION)
TARBALL=$(ROOT)/downloads/Python-$(PYVERSION).tgz
URL=https://www.python.org/ftp/python/$(PYVERSION)/Python-$(PYVERSION).tgz
LIB=libpython$(PYMINOR)$(ABIFLAGS).a

ZLIBVERSION=zlib-1.2.11
ZLIBTARBALL=$(ROOT)/downloads/$(ZLIBVERSION).tar.gz
ZLIBBUILD=$(ROOT)/build/$(ZLIBVERSION)
ZLIBURL=https://zlib.net/$(ZLIBVERSION).tar.gz

ZLIBWASMBUILD=$(ROOT)/build/zlib-wasm/$(ZLIBVERSION)
ZLIBWASM=$(ZLIBWASMBUILD)/libz.a
ZLIBWASMINSTALL=$(INSTALL)/lib/libz.a

SQLITETARBALL=$(ROOT)/downloads/sqlite-autoconf-3270200.tar.gz
SQLITEBUILD=$(ROOT)/build/sqlite-autoconf-3270200
SQLITEURL=https://www.sqlite.org/2019/sqlite-autoconf-3270200.tar.gz


all: $(INSTALL)/lib/$(LIB)


.PHONY: zlib
zlib: $(ZLIBWASMINSTALL)


$(INSTALL)/lib/$(LIB): $(BUILD)/$(LIB)
	( \
		cd $(BUILD); \
		sed -i -e 's/libinstall:.*/libinstall:/' Makefile; \
		touch $(BUILD)/$(LIB) ; \
		make -j 3 HOSTPYTHON=$(HOSTPYTHON) PYTHON_FOR_BUILD=$(HOSTPYTHON) CROSS_COMPILE=yes inclinstall libinstall $(LIB) && \
		cp $(LIB) $(INSTALL)/lib/ && \
		cp $(HOSTINSTALL)/lib/python$(PYMINOR)/`$(HOSTPYTHON) -c "import sysconfig; print(sysconfig._get_sysconfigdata_name())"`.py $(INSTALL)/lib/python$(PYMINOR)/_sysconfigdata__emscripten_.py; \
		sed -i -e 's#'"$(PYODIDE_ROOT)"'##g' $(INSTALL)/lib/python$(PYMINOR)/_sysconfigdata__emscripten_.py; \
	)


clean:
	-rm -fr $(HOSTINSTALL)
	-rm -fr $(BUILD)
	-rm -fr $(INSTALL)


$(TARBALL):
	[ -d $(ROOT)/downloads ] || mkdir $(ROOT)/downloads
	wget -q -O $@ $(URL)
	md5sum --quiet --check checksums || (rm $@; false)


$(ZLIBTARBALL):
	[ -d $(ROOT)/downloads ] || mkdir $(ROOT)/downloads
	wget -q -O $@ $(ZLIBURL)


$(SQLITETARBALL):
	[ -d $(ROOT)/downloads ] || mkdir $(ROOT)/downloads
	wget -q -O $@ $(SQLITEURL)


$(HOSTPYTHON) $(HOSTPGEN): $(TARBALL)
	mkdir -p $(HOSTINSTALL)
	[ -d $(HOSTBUILD) ] || tar -C $(HOSTINSTALL) -xf $(TARBALL)
	( \
		cd $(HOSTBUILD); \
		./configure --prefix=$(HOSTINSTALL) || cat config.log && \
	  make regen-grammar && \
		make install && \
		cp Parser/pgen$(EXE) $(HOSTINSTALL)/bin/ && \
		make distclean \
	)


$(BUILD)/.patched: $(TARBALL)
	[ -d $(BUILD) ] || (mkdir -p $(dir $(BUILD)); tar -C $(dir $(BUILD)) -xf $(TARBALL))
	cat patches/*.patch | (cd $(BUILD) ; patch -p1)
	touch $@


$(ZLIBBUILD)/.patched: $(ZLIBTARBALL)
	[ -d $(ROOT)/build ] || (mkdir $(ROOT)/build)
	tar -C $(ROOT)/build/ -xf $(ROOT)/downloads/zlib-1.2.11.tar.gz
	cat patches/zlib/*.patch | (cd $(ZLIBBUILD) ; patch -p1)
	touch $@


$(SQLITEBUILD)/libsqlite3.la: $(SQLITETARBALL)
	[ -d $(ROOT)/build ] || (mkdir $(ROOT)/build)
	tar -C $(ROOT)/build/ -xf $(SQLITETARBALL)
	( \
		cd $(SQLITEBUILD); \
		emconfigure ./configure; \
		emmake make; \
	)


$(BUILD)/Makefile: $(BUILD)/.patched $(ZLIBBUILD)/.patched $(ZLIBWASMINSTALL)
	cp config.site $(BUILD)/
	( \
		cd $(BUILD); \
		CC=$(WASM_CC) \
		CXX=$(WASM_CXX) \
		AR=$(WASM_AR) \
		RANLIB=$(WASM_RANLIB) \
		CFLAGS=$(WASM_CFLAGS) \
		CXXFLAGS=$(WASM_CFLAGS) \
		CPPFLAGS=$(WASM_CPPFLAGS) \
		LDSHARED=$(WASM_LDSHARED) \
		LDFLAGS=$(WASM_LDFLAGS) \
		CONFIG_SITE=./config.site \
		READELF=true \
		./configure \
		--disable-shared \
		--disable-ipv6 \
		--without-gcc \
		--host=$(WASM_HOST) \
		--build=$(WASM_BUILD) \
		--prefix=$(INSTALL) ; \
	)


$(BUILD)/$(LIB): $(BUILD)/Makefile $(HOSTPYTHON) $(HOSTPGEN) Setup.local
	cp Setup.local $(BUILD)/Modules/
	cat pyconfig.undefs.h >> $(BUILD)/pyconfig.h
	( \
		cp build/$(PYVERSION)/host/lib/python$(PYMINOR)/`$(HOSTPYTHON) -c "import sysconfig; print(sysconfig._get_sysconfigdata_name())"`.py build/$(PYVERSION)/Python-$(PYVERSION)/Lib/_sysconfigdata__emscripten_.py; \
		cd $(BUILD); \
		make -j 3 HOSTPYTHON=$(HOSTPYTHON) HOSTPGEN=$(HOSTPGEN) CROSS_COMPILE=yes $(LIB) \
	)
	touch $(BUILD)/$(LIB)


$(ZLIBWASMINSTALL): $(ZLIBBUILD)/.patched
	[ -d $(ROOT)/build/zlib-wasm ] || (mkdir -p $(ROOT)/build/zlib-wasm)
	tar -C $(ROOT)/build/zlib-wasm -xf $(ROOT)/downloads/$(ZLIBVERSION).tar.gz
	( \
		cd $(ZLIBWASMBUILD); \
		CC=$(WASM_CC) \
		CXX=$(WASM_CXX) \
		AR=$(WASM_AR) \
		RANLIB=$(WASM_RANLIB) \
		CFLAGS=$(WASM_CFLAGS) \
		CXXFLAGS=$(WASM_CFLAGS) \
		CPPFLAGS=$(WASM_CPPFLAGS) \
		LDSHARED=$(WASM_LDSHARED) \
		LDFLAGS=$(WASM_LDFLAGS) \
		./configure \
		--static \
		--prefix=$(INSTALL); \
	)
	( \
		cd $(ZLIBWASMBUILD); \
		make; \
		make install; \
	)

