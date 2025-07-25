# ITF-py: Parser and Encoder for the ITF Trace Format

[![CI](https://github.com/konnov/itf-py/actions/workflows/ci.yml/badge.svg)](https://github.com/konnov/itf-py/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/konnov/itf-py/branch/main/graph/badge.svg)](https://codecov.io/gh/konnov/itf-py)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python library to parse and emit Apalache ITF traces. Refer to [ADR015][] for
the format. ITF traces are emitted by [Apalache][] and [Quint][].

**Intentionally minimalistic.** We keep this library intentionally minimalistic.
You can use it in your projects without worrying about pulling dozens of
dependencies. The package depends on `frozendict` and `frozenlist`.

**Why?** It's much more convenient to manipulate with trace data in an
interactive prompt, similar to SQL.

## Installation

Simply use: `pip install itf-py`.

## Usage

### Deserializing and serializing traces

Assume that you have the following JSON trace stored in the variable
`trace_json`, e.g., as produced by [Apalache][] or [Quint][]:

<!-- name: test_trace -->
```python
trace_json = {
    "#meta": {"id": 23},
    "params": ["N"],
    "vars": ["pc", "x"],
    "loop": 0,
    "states": [
        {
            "#meta": {"no": 0},
            "N": {"#bigint": "3"},
            "pc": "idle",
            "x": {"#bigint": "42"},
        },
        {
            "#meta": {"no": 1},
            "pc": "lock",
            "x": {"#bigint": "43"},
        },
    ],
}
```

We simply import the required function and parse the input:

<!-- name: test_trace -->
```python
from itf_py.itf import ITFState, ITFTrace, trace_from_json
output = trace_from_json(trace_json)
trace = ITFTrace(
    meta={"id": 23},
    params=["N"],
    vars=["pc", "x"],
    loop=0,
    states=[
        ITFState(meta={"no": 0}, values={"N": 3, "pc": "idle", "x": 42}),
        ITFState(meta={"no": 1}, values={"pc": "lock", "x": 43}),
    ],
)
assert output == trace, f"{output} != {trace}"
```

We serialize `trace` back to its JSON form:

<!-- name: test_trace -->
```python
from itf_py.itf import trace_to_json
output = trace_to_json(trace)
assert output == trace_json, f"{output} != {trace_json}"
```

### Deserializing and serializing states

Sometimes, you do not want to deal with whole traces, but only with a single
state. In this case, you can deserialize and serialize states via
`state_from_json` and `state_to_json`:

<!-- name: test_state -->
```python
from itf_py.itf import ITFState, state_from_json, state_to_json
state_json = {
    "#meta": {"no": 1},
    "pc": "lock",
    "x": {"#bigint": "43"},
}
output = state_from_json(state_json)
state = ITFState(meta={"no": 1}, values={"pc": "lock", "x": 43})
assert output == state, f"{output} != {state}"

output = state_to_json(state)
assert output == state_json, f"{output} != {state_json}"
```

### Deserializing and serializing values

Finally, you can work at the level of individual values. The following examples
demonstrate how values of different types are serialized and de-serialized:

<!-- name: test_values -->
```python
from itf_py.itf import value_from_json, value_to_json

# primitive values are easy, except integers are wrapped
assert value_to_json("hello") == "hello"
assert value_from_json("hello") == "hello"
assert value_from_json(True) == True
assert value_to_json(True) == True
assert value_to_json(3) == {"#bigint": "3"}
assert value_from_json({"#bigint": "3"}) == 3

# lists are serialized as JSON arrays
assert value_to_json(["a", "b", "c"]) == ["a", "b", "c"]
# ...and deserialized as frozenlists
from frozenlist import FrozenList
assert value_from_json(["a", "b", "c"]) == FrozenList(["a", "b", "c"])

# tuples are wrapped JSON arrays
assert value_to_json(("a", "b", "c")) == {"#tup": ["a", "b", "c"]}
assert value_from_json({"#tup": ["a", "b", "c"]}) == ("a", "b", "c")

# Sets are serialized as wrapped JSON arrays.
# Be careful, the order in the JSON array may differ!
j = value_to_json(frozenset(["a", "b", "c"]))
assert "#set" in j and len(j["#set"]) == 3
assert "a" in j["#set"] and "b" in j["#set"] and "c" in j["#set"]
# ...and deserialized as frozen sets
assert value_from_json({"#set": ["a", "b", "c"]}) == frozenset(["a", "b", "c"])

# object-like records are serialized as JSON objects
from collections import namedtuple
User = namedtuple("Anon", ["name", "age", "active"])
user = User(name="Alice", age=30, active=True)
output = value_to_json(user)
assert output["name"] == "Alice"
assert output["age"] == {"#bigint": "30"}
assert output["active"] == True
# ...and deserialized as immutable named tuples
output = value_from_json(output)
assert output.name == user.name
assert output.age == user.age
assert output.active == user.active

# Dictionaries are serialized as wrapped JSON arrays of key-value pairs.
# Be careful, the order in the JSON array may differ!
j = value_to_json({"key1": "val1", "key2": "val2"})
assert "#map" in j and len(j["#map"]) == 2
assert ["key1", "val1"] in j["#map"]
assert ["key2", "val2"] in j["#map"]
# ...and deserialized back as frozen dictionaries
from frozendict import frozendict
output = value_from_json({"#map": [["key1", "val1"], ["key2", "val2"]]})
assert output == frozendict({"key1": "val1", "key2": "val2"})

# finally, unserializable values have special representation
from itf_py.itf import ITFUnserializable
output = value_from_json({"#unserializable": "custom-repr"})
assert output == ITFUnserializable("custom-repr")
```


[ADR015]: https://apalache-mc.org/docs/adr/015adr-trace.html
[Apalache]: https://github.com/apalache-mc/apalache
[Quint]: https://github.com/informalsystems/quint
