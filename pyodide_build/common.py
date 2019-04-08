from pathlib import Path

PYODIDE_ROOT = Path(__file__).parents[1].resolve()

CPYTHON_ROOT = PYODIDE_ROOT / 'cpython'
CPYTHON_INSTALL = CPYTHON_ROOT / 'installs' / 'python-3.7.0'
CPYTHON_INCLUDE = CPYTHON_INSTALL / 'include' / 'python3.7d'
CPYTHON_STATIC_LIB = CPYTHON_INSTALL / 'lib' / 'libpython3.7d.a'
CPYTHON_HOST_BUILD = CPYTHON_ROOT / 'build' / '3.7.0' / 'host'

SYSROOT = PYODIDE_ROOT / 'emsdk' / 'emsdk' / 'upstream' / '4778' / 'sysroot'

ROOTDIR = PYODIDE_ROOT / 'tools'
HOSTPYTHON = CPYTHON_HOST_BUILD
TARGETPYTHON = CPYTHON_INSTALL

DEFAULTCFLAGS = ' '.join([
    '--sysroot={}'.format(SYSROOT),
    '-I {}'.format(CPYTHON_INCLUDE),
    '-D__WASM__=1',
])

DEFAULTLDFLAGS = ' '.join([
    "-Xlinker --shared",
    "-Xlinker --import-memory",
    "-Xlinker --import-table",
    "-Xlinker --stack-first",
    "-Xlinker --no-entry",
    str(CPYTHON_STATIC_LIB),
])


def parse_package(package):
    # Import yaml here because pywasmcross needs to run in the built native
    # Python, which won't have PyYAML
    import yaml
    # TODO: Validate against a schema
    with open(package) as fd:
        return yaml.load(fd)
