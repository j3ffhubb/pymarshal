## PyMarshal

pymarshal replicates the feature of (un)marshalling structs in Golang.
Rather than attempting to replicate the exact feature as it exists in Go,
pymarshal aims for elegant, Pythonic simplicity, and to fix the flaws in
Go's implementation such as:
  - extra keys being silently ignored
  - lack of mandatory fields
  - lack of default values

## v2.0.0
Support for the YAML API doc format has been dropped.  If you need this, use
1.6.2

## Currently supported serialization formats
  - [JSON](https://github.com/j3ffhubb/pymarshal/tree/master/examples/usage_json.md)
  - [BSON](https://github.com/j3ffhubb/pymarshal/tree/master/examples/usage_bson.md)
  - [YAML](https://github.com/j3ffhubb/pymarshal/tree/master/examples/usage_yaml.md)
  - [CSV](https://github.com/j3ffhubb/pymarshal/tree/master/examples/usage_csv.md)

As YAML is compatible with JSON, use PyYAML to load or dump data
with the `pymarshal.json` module, there is no explicit YAML module.

## Installation
It is recommended that you install
[from PyPI](https://pypi.python.org/pypi/pymarshal/)
using `pip install pymarshal`

pymarshal is compatible with Python2.7, and Python3.x, althuogh Python2.7
is no longer tested against and is unsupported.

[CLICK HERE](https://github.com/j3ffhubb/pygo) for an example of a
modern REST API that uses PyMarshal

## Overview

The only modification required to your class code is to use the `type_assert`
functions to assign `__init__` arguments to self variables of the same
name.  pymarshal provides the `type_assert` functions to both enforce the type,
and to unmarshal nested objects.

Example:
```python
class MyModel:
    def __init__(
        self,
        a,
        b=5,
    ):
        self.a = type_assert(a, str)
        self.b = type_assert(b, int)

>>> from pymarshal.json import *
>>> x = marshal_json(MyModel("test", 6))
>>> x
{"a": "test", "b": 6}
>>> y = unmarshal_json(x, MyModel)
>>> y.a
"test"
```

NOTE:  Your classes must not implement `__call__` (which is an antipattern
anyway).  Whatever you would've implemented with `__call__` should just be
a normal, named method.

Your `__init__` methods should only use simple assignment through the
`type_assert` functions.  If you have a use-case for a constructor that
does more than simple assignment, use a separate
['factory' static method](https://github.com/j3ffhubb/pymarshal/tree/master/examples/factory.md).

There is also:
  - `type_assert_iter` for iterables
  - `type_assert_dict` for anything that implements .items() -> k, v

Rather than using the Golang "tag" syntax, simply create a
`_marshal_key_swap` and `_unmarshal_key_swap` dict in your class,
and any re-named keys will be swapped before being passed to the
class constructor or before being marshalled to JSON.  The full list
of control variables are documented
[HERE](https://github.com/j3ffhubb/pymarshal/tree/master/examples/control_variables.md).

## Examples

[Examples](https://github.com/j3ffhubb/pymarshal/tree/master/examples/)

