import pytest
from task6 import count_words

def test_word_count_with_file():
    expected_count = 127
    filename = 'task6_read_me.txt'

    try:
        with open(filename, 'r') as f:
            content = f.read()
            assert len(content.split()) == expected_count, "The word count of the file doesn't match the expected value."
    except FileNotFoundError:
        pytest.fail(f"Test failed because '{filename}' was not found.")
        
    actual_count = count_words(filename)
    assert actual_count == expected_count

def test_file_not_found():
    non_existent_file = 'non_existent_file.txt'
    actual_count = count_words(non_existent_file)
    assert actual_count == 0
