import numpy as np
from PIL import Image
import math
from pathlib import Path


def get_probs(img_arr):
    counts = np.bincount(img_arr.flatten(), minlength=256)
    total = np.sum(counts)
    if total == 0:
        return np.zeros(256)
    return counts / total


def calc_entropy(img_arr):
    p = get_probs(img_arr)
    h = 0
    for i in p:
        if i > 0:
            h -= i * math.log2(i)
    return h


def discretize(img_arr, step):
    return img_arr[::step, ::step]


def restore(img_arr, w, h):
    img = Image.fromarray(np.uint8(img_arr))
    restored = img.resize((w, h), Image.Resampling.NEAREST)
    return np.array(restored)


def quantize(img_arr, levels):
    step = 256 / levels
    q = np.floor(img_arr / step) * step
    q = np.clip(q, 0, 255)
    return np.uint8(q)


def calc_kl(p_img, q_img):
    p = get_probs(p_img)
    q = get_probs(q_img)
    kl = 0

    for i in range(256):
        if p[i] > 0:
            q_val = q[i] if q[i] > 0 else 1e-10
            kl += p[i] * math.log2(p[i] / q_val)

    return kl


if __name__ == '__main__':
    img_path = 'input_img/image.jpg'

    try:
        img = Image.open(img_path).convert('L')
    except FileNotFoundError:
        print("Файл не знайдено!")
        exit()

    orig_arr = np.array(img)
    h, w = orig_arr.shape

    base_out_dir = Path('output_img')
    dir_restored = base_out_dir / 'restored'
    dir_quant_discr = base_out_dir / 'quantized_after_discretization'
    dir_quant_orig = base_out_dir / 'quantized_original'

    dir_restored.mkdir(parents=True, exist_ok=True)
    dir_quant_discr.mkdir(parents=True, exist_ok=True)
    dir_quant_orig.mkdir(parents=True, exist_ok=True)

    print(f"Розмір: {w}x{h}")
    orig_h = calc_entropy(orig_arr)
    print(f"Початкова H: {orig_h:.4f}\n")

    steps = [2, 4]
    levels = [8, 16, 64]

    for s in steps:
        print(f"Крок дискретизації: {s}")

        discr = discretize(orig_arr, s)
        restored = restore(discr, w, h)

        restored_path = dir_restored / f"rest_step_{s}.jpg"
        Image.fromarray(restored).save(restored_path)

        h_restored = calc_entropy(restored)
        print(f"H (після відновлення): {h_restored:.4f}\n")

        for l in levels:
            print(f"Квантування на {l} рівнів:")

            quant_img = quantize(restored, l)

            quant_discr_path = dir_quant_discr / f"quant_s{s}_l{l}.jpg"
            Image.fromarray(quant_img).save(quant_discr_path)

            h_quant = calc_entropy(quant_img)
            kl = calc_kl(orig_arr, quant_img)

            print(f"H: {h_quant:.4f}")
            print(f"D(p||q): {kl:.4f}\n")

    print("Квантування оригінального зображення:")
    for l in levels:
        q_orig = quantize(orig_arr, l)

        quant_orig_path = dir_quant_orig / f"quant_orig_{l}.jpg"
        Image.fromarray(q_orig).save(quant_orig_path)

        h_orig = calc_entropy(q_orig)
        kl_orig = calc_kl(orig_arr, q_orig)

        print(f"Рівні: {l} | H: {h_orig:.4f} | D(p||q): {kl_orig:.4f}")