from task2 import get_data_types

def test_integer_type():
    integer_var, _, _, _ = get_data_types()
    assert isinstance(integer_var, int)

def test_float_type():
    _, float_var, _, _ = get_data_types()
    assert isinstance(float_var, float)

def test_string_type():
    _, _, string_var, _ = get_data_types()
    assert isinstance(string_var, str)

def test_boolean_type():
    _, _, _, boolean_var = get_data_types()
    assert isinstance(boolean_var, bool)

def test_variable_values():
    integer_var, float_var, string_var, boolean_var = get_data_types()
    assert integer_var == 10
    assert float_var == 10.5
    assert string_var == "Hello, World!"
    assert boolean_var is True