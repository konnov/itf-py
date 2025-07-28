from itf_py.itf import State, Trace, trace_from_json


class TestTraceFromJson:
    """Test decoding Python traces from JSON."""

    def test_trace_from_json(self):
        """Test decoding a trace"""
        input = {
            "#meta": {"id": 23},
            "params": ["N"],
            "vars": ["pc", "x"],
            "loop": 0,
            "states": [
                {
                    "#meta": {"no": 0},
                    "N": 3,
                    "pc": "init",
                    "x": {"#bigint": "42"},
                },
                {
                    "#meta": {"no": 1},
                    "pc": "lock",
                    "x": {"#bigint": "43"},
                },
            ],
        }
        output = trace_from_json(input)
        expected = Trace(
            meta={"id": 23},
            params=["N"],
            vars=["pc", "x"],
            loop=0,
            states=[
                State(meta={"no": 0}, values={"N": 3, "pc": "init", "x": 42}),
                State(meta={"no": 1}, values={"pc": "lock", "x": 43}),
            ],
        )
        assert output == expected, f"{output} != {expected}"
