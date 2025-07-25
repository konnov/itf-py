from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from frozendict import frozendict
from frozenlist import FrozenList


@dataclass
class ITFState:
    """A single state in an ITF trace as a Python object."""

    meta: Dict[str, Any]
    values: Dict[str, Any]


@dataclass
class ITFTrace:
    """An ITF trace as a Python object."""

    meta: Dict[str, Any]
    params: List[str]
    vars: List[str]
    states: List[ITFState]
    loop: Optional[int]


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
            return frozendict(d)  # immutable dictionary
        elif "#unserializable" in val:
            return ITFUnserializable(value=val["#unserializable"])
        else:
            tup_type = namedtuple("ITFRecord", val.keys())  # type: ignore
            return tup_type(**{k: value_from_json(v) for k, v in val.items()})
    elif isinstance(val, list):
        lst = FrozenList([value_from_json(v) for v in val])
        lst.freeze()  # make it immutable
        return lst
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
    elif isinstance(val, list) or isinstance(val, FrozenList):
        return [value_to_json(v) for v in val]
    elif hasattr(val, "__dict__"):
        return {k: value_to_json(v) for k, v in val.__dict__.items()}
    elif isinstance(val, tuple) and hasattr(val, "_fields"):
        # namedtuple
        return {k: value_to_json(v) for k, v in val._asdict().items()}  # type: ignore
    elif isinstance(val, str):
        return val
    else:
        return ITFUnserializable(value=str(val))


def state_from_json(raw_state: Dict[str, Any]) -> ITFState:
    """Deserialize a single ITFState from JSON"""
    state_meta = raw_state["#meta"] if "#meta" in raw_state else {}
    values = {k: value_from_json(v) for k, v in raw_state.items() if k != "#meta"}
    return ITFState(meta=state_meta, values=values)


def state_to_json(state: ITFState) -> Dict[str, Any]:
    """Serialize a single ITFState to JSON"""
    result = {"#meta": state.meta}
    for k, v in state.values.items():
        result[k] = value_to_json(v)
    return result


def trace_from_json(data: Dict[str, Any]) -> ITFTrace:
    """Deserialize an ITFTrace from JSON"""
    meta = data["#meta"] if "#meta" in data else {}
    params = data.get("params", [])
    vars_ = data["vars"]
    loop = data.get("loop", None)
    states = [state_from_json(s) for s in data["states"]]
    return ITFTrace(meta=meta, params=params, vars=vars_, states=states, loop=loop)


def trace_to_json(trace: ITFTrace) -> Dict[str, Any]:
    """Serialize an ITFTrace to JSON"""
    result: Dict[str, Any] = {"#meta": trace.meta}
    result["params"] = trace.params
    result["vars"] = trace.vars
    result["loop"] = trace.loop
    result["states"] = [state_to_json(s) for s in trace.states]
    return result
