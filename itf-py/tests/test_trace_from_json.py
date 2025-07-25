from itf_py.itf import trace_from_json


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
            ]
        }
        output = trace_from_json(input)
        assert output.meta == {"id": 23}
        assert output.params == ["N"]
        assert output.vars == ["pc", "x"]
        assert output.loop == 0
        assert len(output.states) == 2
        assert output.states[0].meta == {"no": 0}
        assert output.states[0].values == {"N": 3, "pc": "init", "x": 42}
        assert output.states[1].meta == {"no": 1}
        assert output.states[1].values == {"pc": "lock", "x": 43}
