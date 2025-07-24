from types import SimpleNamespace
from itf_py.itf import ITFUnserializable, value_of_itf


class TestValueOfItf:
    """Test parsing ITF values from their JSON representation."""

    def test_value_of_itf_primitives(self):
        """Test decoding primitive values"""
        assert value_of_itf(42) == 42
        assert value_of_itf("hello") == "hello"
        assert value_of_itf(True) == True
        assert value_of_itf(None) == None

    def test_value_of_itf_bigint(self):
        """Test decoding small positive bigint"""
        bigint_val = {"#bigint": "12345"}
        assert value_of_itf(bigint_val) == 12345

    def test_value_of_itf_negative_bigint(self):
        """Test decoding negative bigint values"""
        negative_bigint = {"#bigint": "-98765"}
        assert value_of_itf(negative_bigint) == -98765

    def test_value_of_itf_very_big_bigint(self):
        """Test decoding very big bigint values"""
        big_val = str(2 ** 256 - 1)
        bigint_val = {"#bigint": big_val}
        assert value_of_itf(bigint_val) == 2 ** 256 - 1

    def test_value_of_itf_list(self):
        """Test decoding list values"""
        assert value_of_itf([1, 2, 3]) == [1, 2, 3]
        assert value_of_itf(["a", "b", "c"]) == ["a", "b", "c"]
        assert value_of_itf([]) == []

    def test_value_of_itf_tuple(self):
        """Test decoding tuple values"""
        tup_val = {"#tup": [1, "hello", True]}
        result = value_of_itf(tup_val)
        assert isinstance(result, tuple)
        assert result == (1, "hello", True) 

    def test_value_of_itf_set(self):
        """Test decoding set values"""
        set_val = {"#set": [1, 2, 3]}
        result = value_of_itf(set_val)
        assert isinstance(result, frozenset)
        assert result == frozenset([1, 2, 3])

    def test_value_of_itf_map(self):
        """Test decoding map values"""
        map_val = {"#map": [["key1", "value1"], ["key2", 42]]}
        result = value_of_itf(map_val)
        assert isinstance(result, dict)
        assert result == {"key1": "value1", "key2": 42}

    def test_value_of_itf_nested_structures(self):
        """Test decoding nested data structures"""
        nested_val = {"#set": [{"#bigint": "100"}, {"#tup": ["a", {"#bigint": "200"}]}]}
        result = value_of_itf(nested_val)
        expected = frozenset([100, ("a", 200)])
        assert result == expected

    def test_value_of_itf_record(self):
        """Test decoding a record"""
        dict_val = {"name": "Alice", "age": 30, "active": True}
        result = value_of_itf(dict_val)
        assert result == SimpleNamespace(name="Alice", age=30, active=True)

    def test_value_of_unserializable(self):
        """Test decoding unserializable values"""
        result = value_of_itf({"#unserializable": "custom_object"})
        assert result == ITFUnserializable(value="custom_object")
