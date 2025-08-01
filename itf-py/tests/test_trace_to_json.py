from itf_py.itf import State, Trace, trace_to_json


class TestTraceToJson:
    """Test encoding Python traces to JSON."""

    def test_trace_to_json(self):
        """Test encoding a trace"""
        input = Trace(
            meta={"id": 23},
            params=["N"],
            vars=["pc", "x"],
            loop=0,
            states=[
                State(meta={"no": 0}, values={"N": 3, "pc": "init", "x": 42}),
                State(meta={"no": 1}, values={"pc": "lock", "x": 43}),
            ],
        )
        output = trace_to_json(input)
        expected = {
            "#meta": {"id": 23},
            "params": ["N"],
            "vars": ["pc", "x"],
            "loop": 0,
            "states": [
                {
                    "#meta": {"no": 0},
                    "N": {"#bigint": "3"},
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

        assert output == expected
