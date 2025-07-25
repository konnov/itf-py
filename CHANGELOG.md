## [0.2.1] - 2025-07-25
### Changed

 - Support `from itf_py import ITFTrace, ITFState, trace_to_json, trace_from_json`
 - Support `from itf_py import state_to_json, state_from_json`
 - Support `from itf_py import value_to_json, value_from_json`

## [0.2.0] - 2025-07-25
### Changed

 - Use `frozenlist` to de-serialize lists (sequences, arrays)
 - Use `frozendict` to de-serialize maps
 - Use `namedtuple` to de-serialize records

## [0.1.1] - 2025-07-25
### Added

 - Initial release with the minimal required logic