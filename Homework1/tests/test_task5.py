from task5 import create_books_list, create_student_database

def test_books_list_creation():
    books = create_books_list()
    assert isinstance(books, list)
    assert len(books) == 5
    assert books[0] == ("The Fellowship of the Ring", "J.R.R. Tolkien")

def test_list_slicing_correctness():
    books = create_books_list()
    first_three = books[:3]
    assert len(first_three) == 3
    assert first_three == [
        ("The Fellowship of the Ring", "J.R.R. Tolkien"),
        ("The Two Towers", "J.R.R. Tolkien"),
        ("The Return of the King", "J.R.R. Tolkien")
    ]

def test_student_database_creation():
    student_db = create_student_database()
    assert isinstance(student_db, dict)
    assert len(student_db) == 4
    assert "Alex" in student_db
    assert student_db["Bob"] == "B2"
    assert "C3" in student_db.values()

def test_student_database_keys_and_values():
    student_db = create_student_database()
    expected_keys = {"Alex", "John", "Frank", "Dan"}
    expected_values = {"A1", "B2", "C3", "D4"}
    assert set(student_db.keys()) == expected_keys
    assert set(student_db.values()) == expected_values
