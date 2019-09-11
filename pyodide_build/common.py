from pathlib import Path

PYODIDE_ROOT = Path(__file__).parents[1].resolve()

CPYTHON_ROOT = PYODIDE_ROOT / 'cpython'
CPYTHON_INSTALL = CPYTHON_ROOT / 'installs' / 'python-3.7.0'
CPYTHON_INCLUDE = CPYTHON_INSTALL / 'include' / 'python3.7m'
CPYTHON_STATIC_LIB = CPYTHON_INSTALL / 'lib' / 'libpython3.7m.a'
CPYTHON_HOST_BUILD = CPYTHON_ROOT / 'build' / '3.7.0' / 'host'

SYSROOT = Path('/usr/local/faasm/llvm-sysroot')

ROOTDIR = PYODIDE_ROOT / 'tools'
HOSTPYTHON = CPYTHON_HOST_BUILD
TARGETPYTHON = CPYTHON_INSTALL

# A few things to note about the CFLAGS and LDFLAGS:
#
# - they all have a reason to be there, one mistake and the wasm comes out very different
# - we must NOT include standard libraries
# - we must NOT include the compiled python library
# - everything the c extensions need from these libraries should be included in the main module
# - shared objects must unfortunately export all of their symbols as we don't know ahead of time what we'll need
#
DEFAULTCFLAGS = ' '.join([
    '--sysroot={}'.format(SYSROOT),
    '-I {}'.format(CPYTHON_INCLUDE),
    '--target=wasm32-unknown-emscripten',
    '-DWASM_BUILD=1',
    '-nostdlib',
    '-nostdlib++',
])

DEFAULTLDFLAGS = ' '.join([
    '--sysroot={}'.format(SYSROOT),
    "-Xlinker --shared",
    "-Xlinker --threads",
    "-Xlinker --no-entry",
    "-Xlinker --export-all",
    "-Xlinker --export-dynamic",
    "-Xlinker --no-gc-sections",
    "-Xlinker --stack-first",
    "-Wl,-z,stack-size=2097152 -Wl,",
    '-nostdlib',
    '-nostdlib++',
])


def parse_package(package):
    # Import yaml here because pywasmcross needs to run in the built native
    # Python, which won't have PyYAML
    import yaml
    # TODO: Validate against a schema
    with open(package) as fd:
        return yaml.load(fd)
