import argparse


def lfsr_bits(init_state: list[int], n_bits: int):
    """
    LFSR dla wielomianu x^10 + x^3 + 1.

    Stan ma 10 bitów:
      state[0] = bit najstarszy
      state[9] = bit najmłodszy (wyjściowy)
    """
    state = init_state[:]
    out = []
    for _ in range(n_bits):
        out.append(state[-1])  # bit wyjściowy to LSB
        feedback = state[0] ^ state[7]  # bity odpowiadające x^10 i x^3
        state = [feedback] + state[:-1]  # przesunięcie w prawo
    return out


def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        b = 0
        for j in range(8):
            b |= (bits[i + j] << (7 - j)) if i + j < len(bits) else 0
        out.append(b)
    return bytes(out)


def xor_bytes(data: bytes, keystream_bits: list[int]):
    return bytes(d ^ k for d, k in zip(data, bits_to_bytes(keystream_bits)))


def lfsr_keystream(length_bytes: int):
    init = [1] + [0] * 9
    return lfsr_bits(init, length_bytes * 8)


def encrypt_file(input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()
    enc = xor_bytes(data, lfsr_keystream(len(data)))
    with open(output_path, "wb") as f:
        f.write(enc)
    print(f"Zaszyfrowano: {input_path} → {output_path}")


def decrypt_file(input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()
    dec = xor_bytes(data, lfsr_keystream(len(data)))
    with open(output_path, "wb") as f:
        f.write(dec)
    print(f"Odszyfrowano: {input_path} → {output_path}")


def ex5(plain: bytes):
    cipher = xor_bytes(plain, lfsr_keystream(len(plain)))
    dec = xor_bytes(cipher, lfsr_keystream(len(cipher)))

    print("Plain:", plain)
    print("Cipher (hex):", cipher.hex())
    print("Decrypted:", dec)
    print("Equal:", dec == plain)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--encrypt", nargs=2)
    parser.add_argument("--decrypt", nargs=2)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        ex5(b"Hello, world!")
        print()
        ex5(b"Test123")
    elif args.encrypt:
        encrypt_file(args.encrypt[0], args.encrypt[1])
    elif args.decrypt:
        decrypt_file(args.decrypt[0], args.decrypt[1])
    else:
        parser.print_help()
