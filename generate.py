import os

def generate_test_file(filename="text.txt", target_size_kb=35):
    text_pattern = "МІРОШНІЧЕНКО ЯРОСЛАВ АНДРІЙОВИЧ"
    pattern_size = len(text_pattern.encode("utf-8"))

    target_size_bytes = target_size_kb * 1024
    repeats = (target_size_bytes // pattern_size) + 1

    content = text_pattern * repeats

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    actual_size = os.path.getsize(filename)
    print(f"Файл '{filename}' згенеровано.")
    print(f"Розмір: {actual_size} байт ({actual_size / 1024:.2f} кБ).")

if __name__ == "__main__":
    generate_test_file()