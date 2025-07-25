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

[ADR015]: https://apalache-mc.org/docs/adr/015adr-trace.html
[Apalache]: https://github.com/apalache-mc/apalache
[Quint]: https://github.com/informalsystems/quint
