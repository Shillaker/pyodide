# Building

I've split the Makefile into chunks to make rerunning sections easier. To run from scratch, you can still just run `make`, but the individual bits are as follows:

```
# Set up the host-specific build, needed to run the cross-compile (this should only be needed once)
make host

# Run configure (only need to rerun if changing config)
make configure

# Build the CPython core (run when code has changed)
make build
```

To force a build when code has changed, you can do:

```
rm build/3.7.0/Python-3.7.0/libpython3.7.a
make build
```

# Credits

Based on the hard work of [@dgym](https://github.com/dgym) on
[cpython-emscripten](https://github.com/dgym/cpython-emscripten).
