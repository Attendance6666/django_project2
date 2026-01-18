import string

def analyze_text():
    with open("text.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    line_count = len(lines)
    word_count = 0
    frequency = {}

    for line in lines:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        words = line.split()

        word_count += len(words)

        for word in words:
            frequency[word] = frequency.get(word, 0) + 1

    with open("analysis.txt", "w", encoding="utf-8") as result:
        result.write(f"Total lines: {line_count}\n")
        result.write(f"Total words: {word_count}\n")
        result.write("Word frequency:\n")
        for word, count in frequency.items():
            result.write(f"{word}: {count}\n")


analyze_text()
