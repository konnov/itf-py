from itf_py.itf import state_of_itf


class TestStateOfItf:
    """Test decoding Python states from JSON."""

    def test_state_of_itf(self):
        """Test decoding a state"""
        input = {
            "#meta": {"id": 1},
            "x": {"#bigint": "42"},
            "y": "hello",
        }
        result = state_of_itf(input)
        assert result.meta == {"id": 1}
        assert result.values == {"x": 42, "y": "hello"}
