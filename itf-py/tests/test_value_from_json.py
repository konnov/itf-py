from frozendict import frozendict

from itf_py.itf import ImmutableList, ITFUnserializable, value_from_json


class TestValueFromJson:
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

    def test_value_from_json_set_of_sets(self):
        """Test decoding set of set values"""
        set_val = {"#set": [{"#set": [1, 2]}, {"#set": [3, 4]}]}
        result = value_from_json(set_val)
        assert isinstance(result, frozenset)
        assert len(result) == 2
        assert result == frozenset([frozenset([1, 2]), frozenset([3, 4])])

    def test_value_from_json_set_of_lists(self):
        """Test decoding set of lists values"""
        set_val = {"#set": [[1, 2], [3, 4]]}
        result = value_from_json(set_val)
        assert isinstance(result, frozenset)
        assert len(result) == 2
        list1 = ImmutableList([1, 2])
        list2 = ImmutableList([3, 4])
        assert result == frozenset([list1, list2])

    def test_value_from_json_map(self):
        """Test decoding map values"""
        map_val = {"#map": [["key1", "value1"], ["key2", "value2"]]}
        result = value_from_json(map_val)
        assert isinstance(result, frozendict)
        assert result == frozendict({"key1": "value1", "key2": "value2"})

    def test_value_from_json_set_of_maps(self):
        """Test decoding set of map values"""
        m1 = {"#map": [["key1", "value1"], ["key2", "value2"]]}
        m2 = {"#map": [["key3", "value3"], ["key4", "value4"]]}
        set_of_maps = {"#set": [m1, m2]}
        result = value_from_json(set_of_maps)
        assert isinstance(result, frozenset)
        assert len(result) == 2
        assert result == frozenset(
            [
                frozendict({"key1": "value1", "key2": "value2"}),
                frozendict({"key3": "value3", "key4": "value4"}),
            ]
        )

    def test_value_from_json_nested_structures(self):
        """Test decoding nested data structures"""
        nested_val = {"#set": [{"#bigint": "100"}, {"#tup": ["a", {"#bigint": "200"}]}]}
        result = value_from_json(nested_val)
        expected = frozenset([100, ("a", 200)])
        assert result == expected

    def test_value_from_json_set_of_records(self):
        """Test decoding set of records"""
        r1 = {"a": "f", "b": "g"}
        r2 = {"a": "h", "b": "i"}
        nested_val = {"#set": [r1, r2]}
        result = value_from_json(nested_val)
        expected = frozenset([value_from_json(r) for r in [r1, r2]])
        assert result == expected

    def test_value_from_json_record(self):
        """Test decoding a record"""
        dict_val = {"name": "Alice", "age": 30, "active": True}
        result = value_from_json(dict_val)
        assert result.name == "Alice"
        assert result.age == 30
        assert result.active is True

    def test_value_from_json_tagged_union(self):
        """Test decoding a tagged union"""
        dict_val = {"tag": "Banana", "value": {"length": 5, "color": "yellow"}}
        result = value_from_json(dict_val)
        assert result.__class__.__name__ == "Banana"
        assert result.length == 5
        assert result.color == "yellow"

    def test_value_of_unserializable(self):
        """Test decoding unserializable values"""
        result = value_from_json({"#unserializable": "custom_object"})
        assert result == ITFUnserializable(value="custom_object")
