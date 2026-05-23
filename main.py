import heapq
import itertools
import os
import sys
from collections import Counter, namedtuple


class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"


def build_huffman_tree(text):
    h = []
    counter = itertools.count()

    for ch, freq in Counter(text).items():
        h.append((freq, next(counter), Leaf(ch)))
    heapq.heapify(h)

    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)
        heapq.heappush(h, (freq1 + freq2, next(counter), Node(left, right)))

    code = {}
    if h:
        [(_freq, _count, root)] = h
        root.walk(code, "")
    return code


def shannon_fano_split(symbols, code, acc=""):
    if len(symbols) == 1:
        code[symbols[0][0]] = acc or "0"
        return

    total_freq = sum(freq for _, freq in symbols)
    half_freq = 0
    split_index = 0

    for i, (_, freq) in enumerate(symbols):
        half_freq += freq
        if half_freq >= total_freq / 2:
            split_index = i
            break

    left_part = symbols[:split_index + 1]
    right_part = symbols[split_index + 1:]

    if not right_part:
        left_part = symbols[:split_index]
        right_part = symbols[split_index:]

    shannon_fano_split(left_part, code, acc + "0")
    shannon_fano_split(right_part, code, acc + "1")


def build_shannon_fano_tree(text):
    freqs = Counter(text).most_common()
    code = {}
    if freqs:
        shannon_fano_split(freqs, code)
    return code


def encode_text(text, dictionary):
    return "".join(dictionary[char] for char in text)


def decode_text(encoded_text, dictionary):
    reverse_dict = {v: k for k, v in dictionary.items()}
    decoded = []
    buffer = ""
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_dict:
            decoded.append(reverse_dict[buffer])
            buffer = ""
    return "".join(decoded)


def print_stats(method_name, original_data, original_size, encoded_data, dictionary):
    decoded_data = decode_text(encoded_data, dictionary)
    encoded_bits = len(encoded_data)
    encoded_bytes = encoded_bits / 8
    compression_ratio = original_size / encoded_bytes if encoded_bytes > 0 else 0
    is_success = original_data == decoded_data

    print(f"\n--- {method_name} ---")
    print(f"Стиснено (бітів): {encoded_bits}")
    print(f"Стиснено (байт): {encoded_bytes:.2f}")
    print(f"Коефіцієнт стиснення: {compression_ratio:.2f}")
    print(f"Розкодування успішне: {is_success}")


if __name__ == "__main__":
    file_path = "text.txt"

    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не знайдено.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    if not data:
        print("Файл порожній.")
        sys.exit(1)

    original_size = len(data.encode("utf-8"))
    print(f"Розмір оригінального файлу: {original_size} байт")

    huff_codes = build_huffman_tree(data)
    encoded_huff = encode_text(data, huff_codes)
    print_stats("Метод Хафмена", data, original_size, encoded_huff, huff_codes)

    sf_codes = build_shannon_fano_tree(data)
    encoded_sf = encode_text(data, sf_codes)
    print_stats("Метод Шеннона-Фано", data, original_size, encoded_sf, sf_codes)