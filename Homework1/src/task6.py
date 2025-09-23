def count_words(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return len(content.split())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return 0

if __name__ == "__main__":
    file_to_count = 'task6_read_me.txt'
    word_count = count_words(file_to_count)

    # Check if a word count was actually returned before printing
    if word_count > 0:
        print(f"The file '{file_to_count}' has {word_count} words.")
    else:
        # A more informative message if the count is 0
        print(f"No words to count in '{file_to_count}' (file may be empty or was not found).")