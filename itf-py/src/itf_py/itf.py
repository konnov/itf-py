from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, NoReturn, Optional, SupportsIndex

from frozendict import frozendict


@dataclass
class State:
    """A single state in an ITF trace as a Python object."""

    meta: Dict[str, Any]
    values: Dict[str, Any]


@dataclass
class Trace:
    """An ITF trace as a Python object."""

    meta: Dict[str, Any]
    params: List[str]
    vars: List[str]
    states: List[State]
    loop: Optional[int]


class ImmutableList(list):
    """An immutable wrapper around list that supports hashing,
    yet displays as a list."""

    # frozenlist.FrozenList is what we want, but it does not display
    # nicely in pretty-printing.

    def __init__(self, items: Iterable[Any]):
        super().__init__(items)

    def __hash__(self) -> int:  # type: ignore
        return hash(tuple(self))

    def _forbid_modification(self) -> NoReturn:
        """Forbid modification of the list."""
        raise TypeError("This list is immutable and cannot be modified.")

    def __setitem__(self, _key: Any, _value: Any) -> NoReturn:
        self._forbid_modification()

    def __delitem__(self, _key: Any) -> NoReturn:
        self._forbid_modification()

    def append(self, _value: Any) -> NoReturn:
        self._forbid_modification()

    def extend(self, _values: Iterable[Any]) -> NoReturn:
        self._forbid_modification()

    def insert(self, _index: SupportsIndex, _value: Any) -> None:
        self._forbid_modification()

    def pop(self, _index: SupportsIndex = -1) -> NoReturn:
        self._forbid_modification()

    def remove(self, _value: Any) -> NoReturn:
        self._forbid_modification()

    def clear(self) -> NoReturn:
        self._forbid_modification()

    def reverse(self) -> NoReturn:
        self._forbid_modification()


class ImmutableDict(frozendict):
    """A wrapper around frozendict that displays dictionaries as
    `{k1: v_1, ..., k_n: v_n}`."""

    def __new__(cls, items: Dict[str, Any]) -> Any:
        return super().__new__(cls, items)


ImmutableDict.__str__ = (  # type: ignore
    dict.__str__
)  # use the default dict representation in pretty-printing

ImmutableDict.__repr__ = (  # type: ignore
    dict.__repr__
)  # use the default dict representation in pretty-printing


@dataclass
class ITFUnserializable:
    """A placeholder for unserializable values."""

    value: str


def value_from_json(val: Any) -> Any:
    """Deserialize a Python value from JSON"""
    if isinstance(val, dict):
        if "#bigint" in val:
            return int(val["#bigint"])
        elif "#tup" in val:
            return tuple(value_from_json(v) for v in val["#tup"])
        elif "#set" in val:
            return frozenset(value_from_json(v) for v in val["#set"])
        elif "#map" in val:
            d = {value_from_json(k): value_from_json(v) for (k, v) in val["#map"]}
            return ImmutableDict(d)
        elif "#unserializable" in val:
            return ITFUnserializable(value=val["#unserializable"])
        else:
            ks = val.keys()
            if len(ks) == 2 and "tag" in ks and "value" in ks:
                # This is a tagged union, e.g., {"tag": "Banana", "value": {...}}.
                # Produce Banana(...)
                union_type = namedtuple(val["tag"], val["value"].keys())  # type: ignore
                return union_type(
                    **{k: value_from_json(v) for k, v in val["value"].items()}
                )
            else:
                # This is a general record, e.g., {"field1": ..., "field2": ...}.
                rec_type = namedtuple("Rec", val.keys())  # type: ignore
                return rec_type(**{k: value_from_json(v) for k, v in val.items()})
    elif isinstance(val, list):
        return ImmutableList([value_from_json(v) for v in val])
    else:
        return val  # int, str, bool


def value_to_json(val: Any) -> Any:
    """Serialize a Python value into JSON"""
    if isinstance(val, bool):
        return val
    elif isinstance(val, int):
        return {"#bigint": str(val)}
    elif isinstance(val, tuple) and not hasattr(val, "_fields"):
        return {"#tup": [value_to_json(v) for v in val]}
    elif isinstance(val, frozenset):
        return {"#set": [value_to_json(v) for v in val]}
    elif isinstance(val, dict):
        return {"#map": [[value_to_json(k), value_to_json(v)] for k, v in val.items()]}
    elif isinstance(val, list):
        return [value_to_json(v) for v in val]
    elif hasattr(val, "__dict__"):
        # An object-like structure, e.g., a record, or a union.
        # Note that we cannot distinguish between a record and a tagged union here.
        return {k: value_to_json(v) for k, v in val.__dict__.items()}
    elif isinstance(val, tuple) and hasattr(val, "_fields"):
        # namedtuple
        return {k: value_to_json(v) for k, v in val._asdict().items()}  # type: ignore
    elif isinstance(val, str):
        return val
    else:
        return ITFUnserializable(value=str(val))


def state_from_json(raw_state: Dict[str, Any]) -> State:
    """Deserialize a single State from JSON"""
    state_meta = raw_state["#meta"] if "#meta" in raw_state else {}
    values = {k: value_from_json(v) for k, v in raw_state.items() if k != "#meta"}
    return State(meta=state_meta, values=values)


def state_to_json(state: State) -> Dict[str, Any]:
    """Serialize a single State to JSON"""
    result = {"#meta": state.meta}
    for k, v in state.values.items():
        result[k] = value_to_json(v)
    return result


def trace_from_json(data: Dict[str, Any]) -> Trace:
    """Deserialize a Trace from JSON"""
    meta = data["#meta"] if "#meta" in data else {}
    params = data.get("params", [])
    vars_ = data["vars"]
    loop = data.get("loop", None)
    states = [state_from_json(s) for s in data["states"]]
    return Trace(meta=meta, params=params, vars=vars_, states=states, loop=loop)


def trace_to_json(trace: Trace) -> Dict[str, Any]:
    """Serialize a Trace to JSON"""
    result: Dict[str, Any] = {"#meta": trace.meta}
    result["params"] = trace.params
    result["vars"] = trace.vars
    result["loop"] = trace.loop
    result["states"] = [state_to_json(s) for s in trace.states]
    return result
