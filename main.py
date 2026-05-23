from reedsolo import RSCodec

def write_data_to_file(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

def main():
    ecc_symbols = 4
    rs = RSCodec(ecc_symbols)

    original_text = "Data_MSG"
    data_bytes = bytearray(original_text, "utf-8")

    write_data_to_file("data.txt", data_bytes)
    print(f"1. Початкові дані: {original_text} (байти: {list(data_bytes)})")

    encoded_bytes = rs.encode(data_bytes)
    write_data_to_file("code.txt", encoded_bytes)
    print(f"2. Закодовані дані з контрольними символами: {list(encoded_bytes)}")

    corrupted_bytes = bytearray(encoded_bytes)
    corrupted_bytes[0] = ord("E")
    corrupted_bytes[1] = ord("R")

    print(f"3. Спотворені дані (імітація завад): {list(corrupted_bytes)}")
    print(f"   Текст з помилками: {corrupted_bytes[:8].decode('utf-8', errors='ignore')}")

    try:
        decoded_bytes, _, err_positions = rs.decode(corrupted_bytes)
        write_data_to_file("decode.txt", decoded_bytes)

        decoded_text = decoded_bytes.decode("utf-8")
        print(f"4. Успішне декодування! Відновлені дані: {decoded_text}")
        print(f"   Декодер знайшов помилки на позиціях: {list(err_positions)}")

    except Exception as e:
        print(f"[!] Помилка декодування: {e}")

if __name__ == "__main__":
    main()