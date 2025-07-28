# ITF-py: Parser and Encoder for the ITF Trace Format

Python library to parse and emit Apalache ITF traces. Refer to [ADR015][] for
the format. ITF traces are emitted by [Apalache][] and [Quint][].

**Intentionally minimalistic.** We keep this library intentionally minimalistic.
You can use it in your projects without worrying about pulling dozens of
dependencies. The package depends on `frozendict`.

**Why?** It's much more convenient to manipulate with trace data in an
interactive prompt, similar to SQL.

See usage examples on the [itf-py][] page on Github.

**Alternatives.** If you need to deserialize/serialize ITF traces in Rust, check
[itf-rs][].

[ADR015]: https://apalache-mc.org/docs/adr/015adr-trace.html
[Apalache]: https://github.com/apalache-mc/apalache
[Quint]: https://github.com/informalsystems/quint
[itf-rs]: https://github.com/informalsystems/itf-rs
[itf-py]: https://github.com/konnov/itf-py