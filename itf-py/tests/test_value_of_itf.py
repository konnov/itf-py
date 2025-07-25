from types import SimpleNamespace

from itf_py.itf import ITFUnserializable, value_from_json


class TestValueOfItf:
    """Test parsing ITF values from their JSON representation."""

    def test_value_from_json_primitives(self):
        """Test decoding primitive values"""
        assert value_from_json(42) == 42
        assert value_from_json("hello") == "hello"
        assert value_from_json(True) == True
        assert value_from_json(None) == None

    def test_value_from_json_bigint(self):
        """Test decoding small positive bigint"""
        bigint_val = {"#bigint": "12345"}
        assert value_from_json(bigint_val) == 12345

    def test_value_from_json_negative_bigint(self):
        """Test decoding negative bigint values"""
        negative_bigint = {"#bigint": "-98765"}
        assert value_from_json(negative_bigint) == -98765

    def test_value_from_json_very_big_bigint(self):
        """Test decoding very big bigint values"""
        big_val = str(2**256 - 1)
        bigint_val = {"#bigint": big_val}
        assert value_from_json(bigint_val) == 2**256 - 1

    def test_value_from_json_list(self):
        """Test decoding list values"""
        assert value_from_json([1, 2, 3]) == [1, 2, 3]
        assert value_from_json(["a", "b", "c"]) == ["a", "b", "c"]
        assert value_from_json([]) == []

    def test_value_from_json_tuple(self):
        """Test decoding tuple values"""
        tup_val = {"#tup": [1, "hello", True]}
        result = value_from_json(tup_val)
        assert isinstance(result, tuple)
        assert result == (1, "hello", True)

    def test_value_from_json_set(self):
        """Test decoding set values"""
        set_val = {"#set": [1, 2, 3]}
        result = value_from_json(set_val)
        assert isinstance(result, frozenset)
        assert result == frozenset([1, 2, 3])

    def test_value_from_json_map(self):
        """Test decoding map values"""
        map_val = {"#map": [["key1", "value1"], ["key2", 42]]}
        result = value_from_json(map_val)
        assert isinstance(result, dict)
        assert result == {"key1": "value1", "key2": 42}

    def test_value_from_json_nested_structures(self):
        """Test decoding nested data structures"""
        nested_val = {"#set": [{"#bigint": "100"}, {"#tup": ["a", {"#bigint": "200"}]}]}
        result = value_from_json(nested_val)
        expected = frozenset([100, ("a", 200)])
        assert result == expected

    def test_value_from_json_record(self):
        """Test decoding a record"""
        dict_val = {"name": "Alice", "age": 30, "active": True}
        result = value_from_json(dict_val)
        assert result == SimpleNamespace(name="Alice", age=30, active=True)

    def test_value_of_unserializable(self):
        """Test decoding unserializable values"""
        result = value_from_json({"#unserializable": "custom_object"})
        assert result == ITFUnserializable(value="custom_object")
