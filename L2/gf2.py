# Logarytmy Zecha dla GF(2^m)
ZECH = {
    4:  [None, 2, 1],
    8:  [None, 3, 6, 1, 5, 4, 2],
    16: [None, 4, 8, 14, 1, 10, 13, 9, 2, 7, 5, 12, 11, 6, 3],
}

def lab(q):
    return [("0" if v == 0 else ("1" if v == 1 else f"a{v-1}")) for v in range(q)]

def P_pow(x, y, q):
    if x == 0 or y == 0:
        return 0
    return ((x + y - 2) % (q - 1)) + 1

def print_mul_pow(q):
    L = lab(q)
    print(f"\nMnożenie w GF(2^{ {8:3,16:4}[q] })")
    w = max(len(s) for s in L) + 2
    print("".join(s.center(w) for s in [" "] + L))
    for x in range(q):
        row = [L[x].center(w)]
        for y in range(q):
            row.append(L[P_pow(x, y, q)].center(w))
        print("".join(row))

# -------- Zadania 2–4: operacje z logarytmami Zecha ------------

def S(x, y, q):  # Dodawanie
    if x == 0 or y == 0:
        return x + y
    if x == y:
        return 0
    if x < y:
        x, y = y, x
    z = ZECH[q][x - y]
    return ((y + z - 1) % (q - 1)) + 1

def P(x, y, q):  # Mnożenie
    if x == 0 or y == 0:
        return 0
    return ((x + y - 2) % (q - 1)) + 1

def print_table(op, q):
    name = "Mnożenie" if op == "mul" else "Dodawanie"
    L = lab(q)
    print(f"\n{name} w GF(2^{ {4:2,8:3,16:4}[q] }) z logarytmami Zecha")
    header = [" "] + L
    w = max(len(s) for s in L) + 2
    print("".join(s.center(w) for s in header))
    for x in range(q):
        row = []
        for y in range(q):
            v = P(x, y, q) if op == "mul" else S(x, y, q)
            row.append(L[v])
        print("".join([L[x].center(w)] + [c.center(w) for c in row]))


def poly4_GF16(x1, x2, x3, x4):
    q = 16

    A = S(S(x1, x2, q), S(x3, x4, q), q)

    pairs = [
        (x1, x2), (x1, x3), (x1, x4),
        (x2, x3), (x2, x4), (x3, x4)
    ]
    B = 0
    for a, b in pairs:
        B = S(B, P(a, b, q), q)

    triples = [
        (x1, x2, x3), (x1, x2, x4),
        (x1, x3, x4), (x2, x3, x4)
    ]
    C = 0
    for a, b, c in triples:
        C = S(C, P(P(a, b, q), c, q), q)

    D = P(P(P(x1, x2, q), x3, q), x4, q)

    return A, B, C, D


def print_poly_GF16(x1, x2, x3, x4):
    L = lab(16)
    A, B, C, D = poly4_GF16(x1, x2, x3, x4)

    print("\nWielomian czwartego stopnia w GF(2^4):")
    print(f"W(x) = x^4 + {L[A]} x^3 + {L[B]} x^2 + {L[C]} x + {L[D]}")


def main():
    # Zadanie 1: tablice mnozenia GF(2^3) i GF(2^4)
    print("\n=== Zadanie 1: Tablice mnożenia ===")
    print_mul_pow(8)
    print_mul_pow(16)

    # Zadanie 2–4: tablice dodawania i mnożenia z Zecha
    print("\n=== Zadania 2-4: Dodawanie i mnożenie z logarytmami Zecha ===")
    for a in ("mul", "add"):
        for q in (4, 8, 16):
            print_table(a, q)

    print("\nCzęść interaktywna (zadanie 2)")
    try:
        q = int(input("Wybierz q z {4,8,16}: "))
        if q not in (4, 8, 16):
            raise ValueError
        x = int(input(f"x w 0..{q-1}: "))
        y = int(input(f"y w 0..{q-1}: "))
        if not (0 <= x < q and 0 <= y < q):
            raise ValueError

        L = lab(q)
        sx = S(x, y, q)
        px = P(x, y, q)
        print(f"x + y = {sx} ({L[sx]})")
        print(f"x * y = {px} ({L[px]})")
    except Exception:
        print("Błędne dane.")

    print("\n=== Zadanie 5: Wielomian czwartego stopnia w GF(16) ===")
    try:
        print("Podaj elementy x1, x2, x3, x4 z zakresu 0..15 (GF(16))")
        x1 = int(input("x1 = "))
        x2 = int(input("x2 = "))
        x3 = int(input("x3 = "))
        x4 = int(input("x4 = "))
        if not all(0 <= v < 16 for v in (x1, x2, x3, x4)):
            raise ValueError
        print_poly_GF16(x1, x2, x3, x4)
    except Exception:
        print("Błędne dane.")


if __name__ == "__main__":
    main()
