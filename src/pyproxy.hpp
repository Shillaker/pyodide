#ifndef PYPROXY_H
#define PYPROXY_H

#include <emscripten.h>
#include <emscripten/bind.h>
#include <emscripten/val.h>
#include <Python.h>

#include "js2python.hpp"
#include "python2js.hpp"

class Py {
  PyObject *x;

public:
  Py(PyObject *obj);
  Py(const Py& o);
  ~Py();

  emscripten::val call(emscripten::val args, emscripten::val kwargs);
  emscripten::val getattr(emscripten::val idx);
  void setattr(emscripten::val idx, emscripten::val v);
  emscripten::val getitem(emscripten::val idx);
  void setitem(emscripten::val idx, emscripten::val v);
};

#endif /* PYPROXY_H */