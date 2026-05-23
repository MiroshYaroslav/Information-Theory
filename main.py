def read_config(filename="config.txt"):
    default_r = 4
    default_info = "10110101101"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

            if not lines:
                raise ValueError("Файл порожній")

            r = int(lines[0])
            info_block = lines[1] if len(lines) > 1 else default_info
            return r, info_block

    except Exception as e:
        print(f"Помилка зчитування: {e}. Використовуємо значення за замовчуванням.")
        return default_r, default_info


def get_code_parameters(r):
    n = (1 << r) - 1
    k = n - r
    return n, k


def print_parity_relations(r, n):
    print("--- Перевірні співвідношення ---")
    for i in range(r):
        parity_pos = 1 << i
        involved_bits = []
        for j in range(parity_pos + 1, n + 1):
            if j & parity_pos:
                involved_bits.append(f"біт_{j}")
        print(f"p{parity_pos} = " + " ⊕ ".join(involved_bits))
    print()


def encode_hamming(data_bits, r, n):
    encoded = [0] * (n + 1)
    j = 0

    for i in range(1, n + 1):
        if not (i & (i - 1) == 0):
            encoded[i] = int(data_bits[j])
            j += 1

    for i in range(r):
        parity_pos = 1 << i
        parity_val = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity_val ^= encoded[j]
        encoded[parity_pos] = parity_val

    return encoded[1:]


def introduce_error(encoded_data, error_pos):
    corrupted_data = list(encoded_data)
    if 1 <= error_pos <= len(encoded_data):
        corrupted_data[error_pos - 1] ^= 1
    return corrupted_data


def decode_hamming(received_data, r, n):
    received = [0] + received_data
    syndrome = 0

    for i in range(r):
        parity_pos = 1 << i
        parity_val = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity_val ^= received[j]
        if parity_val:
            syndrome += parity_pos

    if syndrome == 0:
        print("Помилок не виявлено.")
        return received[1:]
    else:
        print(f"Виявлено помилку в розряді: {syndrome}")
        received[syndrome] ^= 1
        print("Помилку успішно виправлено!")
        return received[1:]


if __name__ == "__main__":
    r, info_block = read_config()
    n, k = get_code_parameters(r)

    print(f"Параметри коду: r = {r}, n = {n}, k = {k} (Довжина коду = {n}, інфо-бітів = {k})\n")

    print_parity_relations(r, n)

    if len(info_block) < k:
        info_block = info_block.ljust(k, '0')
    elif len(info_block) > k:
        info_block = info_block[:k]

    print(f"Початковий інфо-блок: {info_block}")

    encoded_message = encode_hamming(info_block, r, n)
    print(f"Закодоване повідомлення: {encoded_message}")

    error_index = 6
    corrupted_message = introduce_error(encoded_message, error_index)
    print(f"Повідомлення з помилкою:   {corrupted_message}")

    corrected_message = decode_hamming(corrupted_message, r, n)
    print(f"Виправлене повідомлення: {corrected_message}")