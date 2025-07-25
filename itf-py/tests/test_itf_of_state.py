from itf_py.itf import ITFState, itf_of_state


class TestItfOfState:
    """Test encoding Python states to JSON."""

    def test_itf_of_state(self):
        """Test encoding a state"""
        state = ITFState(meta={"id": 1}, values={"x": 42, "y": "hello"})
        result = itf_of_state(state)
        assert result == {
            "#meta": {"id": 1},
            "x": {"#bigint": "42"},
            "y": "hello",
        }
