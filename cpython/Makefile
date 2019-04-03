PYODIDE_ROOT=$(abspath ..)
include ../Makefile.envs

ROOT=$(abspath .)

# We need to make sure the host python build the first on the path
PATH:=$(ROOT)/build/$(PYVERSION)/host/bin:$(PATH)

CONF_BUILD=wasm32
CONF_HOST=wasm32-unknown-wasm

HOSTINSTALL=$(ROOT)/build/$(PYVERSION)/host
HOSTBUILD=$(HOSTINSTALL)/Python-$(PYVERSION)
HOSTPYTHON=$(HOSTINSTALL)/bin/python3$(EXE)
HOSTPGEN=$(HOSTINSTALL)/bin/pgen$(EXE)

BUILD=$(ROOT)/build/$(PYVERSION)/Python-$(PYVERSION)
INSTALL=$(ROOT)/installs/python-$(PYVERSION)
TARBALL=$(ROOT)/downloads/Python-$(PYVERSION).tgz
URL=https://www.python.org/ftp/python/$(PYVERSION)/Python-$(PYVERSION).tgz
LIB=libpython$(PYMINOR).a

ZLIBVERSION = 1.2.11
ZLIBTARBALL=$(ROOT)/downloads/zlib-$(ZLIBVERSION).tar.gz
ZLIBBUILD=$(ROOT)/build/zlib-$(ZLIBVERSION)
ZLIBURL=https://zlib.net/zlib-1.2.11.tar.gz


all: host configure build

# Sets up the host build (run once)
.PHONY: host
host: $(HOSTPYTHON) $(HOSTPGEN) $(BUILD)/.patched $(ZLIBBUILD)/.patched

# Configures the build
.PHONY: configure
configure: $(BUILD)/Makefile

# Runs the build 
.PHONY: build
build: $(INSTALL)/lib/$(LIB)


clean:
	-rm -fr $(HOSTINSTALL)
	-rm -fr $(BUILD)
	-rm -fr $(INSTALL)

# ---------------------------------
# WASM BUILD
# ---------------------------------

# Build libs
$(INSTALL)/lib/$(LIB): $(BUILD)/$(LIB)
	( \
		cd $(BUILD); \
		sed -i -e 's/libinstall:.*/libinstall:/' Makefile; \
		touch $(BUILD)/$(LIB) ; \
		emmake make -j 4 HOSTPYTHON=$(HOSTPYTHON) PYTHON_FOR_BUILD=$(HOSTPYTHON) CROSS_COMPILE=yes inclinstall libinstall $(LIB) && \
		cp $(LIB) $(INSTALL)/lib/ && \
		cp $(HOSTINSTALL)/lib/python$(PYMINOR)/`$(HOSTPYTHON) -c "import sysconfig; print(sysconfig._get_sysconfigdata_name())"`.py $(INSTALL)/lib/python$(PYMINOR)/_sysconfigdata__emscripten_.py; \
		sed -i -e 's#'"$(PYODIDE_ROOT)"'##g' $(INSTALL)/lib/python$(PYMINOR)/_sysconfigdata__emscripten_.py; \
	)

# Configure
$(BUILD)/Makefile:
	echo "PATH: $(PATH)" 
	cp config.site $(BUILD)/
	( \
		cd $(BUILD); \
		CONFIG_SITE=./config.site READELF=true emconfigure ./configure --with-pydebug --without-pymalloc --disable-shared --disable-ipv6 --without-gcc --host=$(CONF_HOST) --build=$(CONF_BUILD) --prefix=$(INSTALL) ; \
	)

# Build core
$(BUILD)/$(LIB): $(BUILD)/Makefile Setup.local
	cp Setup.local $(BUILD)/Modules/
	cat pyconfig.undefs.h >> $(BUILD)/pyconfig.h
	( \
		cp build/$(PYVERSION)/host/lib/python$(PYMINOR)/`$(HOSTPYTHON) -c "import sysconfig; print(sysconfig._get_sysconfigdata_name())"`.py build/$(PYVERSION)/Python-$(PYVERSION)/Lib/_sysconfigdata__emscripten_.py; \
		cd $(BUILD); \
		emmake make -j 4 HOSTPYTHON=$(HOSTPYTHON) HOSTPGEN=$(HOSTPGEN) CROSS_COMPILE=yes $(LIB) \
	)
	touch $(BUILD)/$(LIB)


# ----------------------------------
# DOWNLOAD AND HOST BUILD (RUN ONCE)
# ----------------------------------

$(TARBALL):
	[ -d $(ROOT)/downloads ] || mkdir $(ROOT)/downloads
	wget -q -O $@ $(URL)
	md5sum --quiet --check checksums || (rm $@; false)


$(ZLIBTARBALL):
	[ -d $(ROOT)/downloads ] || mkdir $(ROOT)/downloads
	wget -q -O $@ $(ZLIBURL)


$(ZLIBBUILD)/.patched: $(ZLIBTARBALL)
	[ -d $(ROOT)/build ] || (mkdir $(ROOT)/build)
	tar -C $(ROOT)/build/ -xf $(ROOT)/downloads/zlib-1.2.11.tar.gz
	cat patches/zlib/*.patch | (cd $(ZLIBBUILD) ; patch -p1)
	touch $@


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

# Patches the downloaded code
$(BUILD)/.patched: $(TARBALL)
	[ -d $(BUILD) ] || (mkdir -p $(dir $(BUILD)); tar -C $(dir $(BUILD)) -xf $(TARBALL))
	cat patches/*.patch | (cd $(BUILD) ; patch -p1)
	touch $@


