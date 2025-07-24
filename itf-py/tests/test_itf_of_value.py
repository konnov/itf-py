from types import SimpleNamespace

from itf_py.itf import itf_of_value


class TestItfOfValue:
    """Test encoding Python values to JSON."""

    def test_itf_of_value_primitives(self):
        """Test encoding primitive values"""
        assert itf_of_value(42) == {"#bigint": "42"}
        assert itf_of_value("hello") == "hello"
        assert itf_of_value(True) == True

    def test_itf_of_value_bigint(self):
        """Test encoding small positive bigint"""
        assert itf_of_value(12345) == {"#bigint": "12345"}

    def test_itf_of_value_negative_bigint(self):
        """Test encoding negative bigint values"""
        assert itf_of_value(-98765) == {"#bigint": "-98765"}

    def test_itf_of_value_very_big_bigint(self):
        """Test encoding very big bigint values"""
        big_val = str(2**256 - 1)
        assert itf_of_value(2**256 - 1) == {"#bigint": big_val}

    def test_itf_of_value_list(self):
        """Test encoding list values"""
        assert itf_of_value([1, 2, 3]) == [
            itf_of_value(1),
            itf_of_value(2),
            itf_of_value(3),
        ]
        assert itf_of_value(["a", "b", "c"]) == ["a", "b", "c"]
        assert itf_of_value([]) == []

    def test_itf_of_value_tuple(self):
        """Test encoding tuple values"""
        assert itf_of_value((1, "hello", True)) == {
            "#tup": [itf_of_value(1), "hello", True]
        }

    def test_itf_of_value_set(self):
        """Test encoding set values"""
        assert itf_of_value(frozenset([1, 2, 3])) == {
            "#set": [itf_of_value(1), itf_of_value(2), itf_of_value(3)]
        }

    def test_itf_of_value_map(self):
        """Test encoding map values"""
        assert itf_of_value({"key1": "value1", "key2": 42}) == {
            "#map": [["key1", "value1"], ["key2", itf_of_value(42)]]
        }

    def test_itf_of_value_nested_structures(self):
        """Test encoding nested data structures"""
        result = itf_of_value(frozenset([100, ("a", 200)]))
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
        user = SimpleNamespace(name="Alice", age=30, active=True)
        result = itf_of_value(user)
        assert result == {"name": "Alice", "age": itf_of_value(30), "active": True}
