from collections import namedtuple
from types import SimpleNamespace

from itf_py.itf import value_to_json


class TestValueToJson:
    """Test encoding Python values to JSON."""

    def test_value_to_json_primitives(self):
        """Test encoding primitive values"""
        assert value_to_json(42) == {"#bigint": "42"}
        assert value_to_json("hello") == "hello"
        assert value_to_json(True) == True

    def test_value_to_json_bigint(self):
        """Test encoding small positive bigint"""
        assert value_to_json(12345) == {"#bigint": "12345"}

    def test_value_to_json_negative_bigint(self):
        """Test encoding negative bigint values"""
        assert value_to_json(-98765) == {"#bigint": "-98765"}

    def test_value_to_json_very_big_bigint(self):
        """Test encoding very big bigint values"""
        big_val = str(2**256 - 1)
        assert value_to_json(2**256 - 1) == {"#bigint": big_val}

    def test_value_to_json_list(self):
        """Test encoding list values"""
        assert value_to_json([1, 2, 3]) == [
            value_to_json(1),
            value_to_json(2),
            value_to_json(3),
        ]
        assert value_to_json(["a", "b", "c"]) == ["a", "b", "c"]
        assert value_to_json([]) == []

    def test_value_to_json_tuple(self):
        """Test encoding tuple values"""
        assert value_to_json((1, "hello", True)) == {
            "#tup": [value_to_json(1), "hello", True]
        }

    def test_value_to_json_set(self):
        """Test encoding set values"""
        assert value_to_json(frozenset([1, 2, 3])) == {
            "#set": [value_to_json(1), value_to_json(2), value_to_json(3)]
        }

    def test_value_to_json_map(self):
        """Test encoding map values"""
        assert value_to_json({"key1": "value1", "key2": 42}) == {
            "#map": [["key1", "value1"], ["key2", value_to_json(42)]]
        }

    def test_value_to_json_nested_structures(self):
        """Test encoding nested data structures"""
        result = value_to_json(frozenset([100, ("a", 200)]))
        # Since sets are unordered, we need to check the result more carefully
        assert "#set" in result
        result_set = result["#set"]
        assert len(result_set) == 2

        # Check that both expected elements are present
        bigint_elem = {"#bigint": "100"}
        tuple_elem = {"#tup": ["a", {"#bigint": "200"}]}
        assert bigint_elem in result_set
        assert tuple_elem in result_set

    def test_itf_of_named_value(self):
        """Test encoding a record"""
        User = namedtuple("User", ["name", "age", "active"])
        user = User(name="Alice", age=30, active=True)
        result = value_to_json(user)
        assert result == {"name": "Alice", "age": value_to_json(30), "active": True}
