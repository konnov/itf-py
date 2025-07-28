from itf_py.itf import State, state_to_json


class TestStateToJson:
    """Test encoding Python states to JSON."""

    def test_state_to_json(self):
        """Test encoding a state"""
        state = State(meta={"id": 1}, values={"x": 42, "y": "hello"})
        result = state_to_json(state)
        assert result == {
            "#meta": {"id": 1},
            "x": {"#bigint": "42"},
            "y": "hello",
        }
