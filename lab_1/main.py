from PIL import Image
import math
import heapq
from collections import Counter


class Node:
    def __init__(self, prob, symbol=None, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.prob < other.prob


def calc_entropy(image_path):
    try:
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print("File not found")
        return None, None

    pixels = list(img.tobytes())
    total = len(pixels)

    counts = Counter(pixels)
    probs = {p: c / total for p, c in counts.items()}

    entropy = 0
    for p in probs.values():
        if p > 0:
            entropy -= p * math.log2(p)

    print(f"N: {total}")
    print(f"K: {len(counts)}")
    print(f"H: {entropy:.4f}")

    return probs, entropy


def build_tree(probs):
    heap = [Node(p, sym) for sym, p in probs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(left.prob + right.prob, left=left, right=right)
        heapq.heappush(heap, parent)

    return heap[0]


def get_codes(node, current="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.symbol is not None:
        codes[node.symbol] = current
        return codes

    get_codes(node.left, current + "0", codes)
    get_codes(node.right, current + "1", codes)

    return codes


def eval_huffman(probs, codes, h):
    L = sum(probs[sym] * len(code) for sym, code in codes.items())
    print(f"L: {L:.4f}")
    print(f"Lm: {h:.4f}")
    print(f"L - Lm: {L - h:.4f}")


def encode_blocks(pixels, h, block_size=2):
    print(f"\nBlock coding ({block_size} px)")
    blocks = [tuple(pixels[i:i + block_size]) for i in range(0, len(pixels) - block_size + 1, block_size)]
    total_blocks = len(blocks)

    counts = Counter(blocks)
    probs = {b: c / total_blocks for b, c in counts.items()}

    tree = build_tree(probs)
    codes = get_codes(tree)

    L_block = sum(probs[b] * len(code) for b, code in codes.items())
    L_per_pixel = L_block / block_size

    print(f"Unique blocks: {len(counts)}")
    print(f"L per block: {L_block:.4f}")
    print(f"L per pixel: {L_per_pixel:.4f}")
    print(f"Lm: {h:.4f}")
    print(f"Difference: {L_per_pixel - h:.4f}")


if __name__ == '__main__':
    img_path = 'image_2.bmp'
    p, h = calc_entropy(img_path)

    if p is not None and h is not None:
        print("\nHuffman")
        tree = build_tree(p)
        codes = get_codes(tree)

        for sym in list(codes.keys())[:5]:
            print(f"Pixel {sym:3} -> {codes[sym]}")

        eval_huffman(p, codes, h)

        img = Image.open(img_path).convert('L')
        raw_pixels = list(img.tobytes())
        encode_blocks(raw_pixels, h, 2)