def create_books_list():
    return [
        ("The Fellowship of the Ring", "J.R.R. Tolkien"),
        ("The Two Towers", "J.R.R. Tolkien"),
        ("The Return of the King", "J.R.R. Tolkien"),
        ("The Hobbit", "J.R.R. Tolkien"),
        ("Dune", "Frank Herbert")
    ]

def print_first_three_books(books):
    print("First three books:")
    for book in books[:3]:
        print(f"Title: {book[0]}, Author: {book[1]}")

def create_student_database():
    return {
        "Alice": "A1",
        "Bob": "B2",
        "Charlie": "C3",
        "Diana": "D4"
    }

if __name__ == "__main__":
    # Part 1: Lists
    my_books = create_books_list()
    print_first_three_books(my_books)

    print("\n" + "="*20 + "\n")

    # Part 2: Dictionaries
    student_db = create_student_database()
    print("Student Database:")
    for name, student_id in student_db.items():
        print(f"Name: {name}, Student ID: {student_id}")
