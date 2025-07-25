# ITF-py: Parser and Encoder for the ITF Trace Format

[![CI](https://github.com/konnov/itf-py/actions/workflows/ci.yml/badge.svg)](https://github.com/konnov/itf-py/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/konnov/itf-py/branch/main/graph/badge.svg)](https://codecov.io/gh/konnov/itf-py)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python library to parse and emit Apalache ITF traces. Refer to [ADR015][] for
the format. ITF traces are emitted by [Apalache][] and [Quint][].

**Intentionally minimalistic.** We keep this library intentionally minimalistic.
You can use it in your projects without worrying about pulling dozens of
dependencies.

## Installation

Simply use: `pip install itf-py`.

## Usage

### Deserializing and serializing traces

Assume that you have the following JSON trace stored in the variable `input`,
e.g., as produced by [Apalache][] or [Quint][]:

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


[ADR015]: https://apalache-mc.org/docs/adr/015adr-trace.html
[Apalache]: https://github.com/apalache-mc/apalache
[Quint]: https://github.com/informalsystems/quint
