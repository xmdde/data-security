def gf_tables(p: int):
    add = [[(i + j) % p for j in range(p)] for i in range(p)]
    mul = [[(i * j) % p for j in range(p)] for i in range(p)]
    add_inv = {i: (-i) % p for i in range(p)}
    mul_inv = {i: (None if i == 0 else pow(i, p - 2, p)) for i in range(p)}
    return add, mul, add_inv, mul_inv


def ex1() -> None:
    primes: list[int] = [3, 5, 7]
    for p in primes:
        print(f"\n===== GF({p}) =====")
        add, mul, add_inv, mul_inv = gf_tables(p)

        print("Dodawanie:")
        for row in add:
            print(row)

        print("Mnożenie:")
        for row in mul:
            print(row)

        print("Elementy przeciwne:", add_inv)
        print("Elementy odwrotne:", mul_inv)


def mult_order(a: int, p: int) -> int:
    if a % p == 0:
        return None
    val: int = a % p
    order: int = 1
    while val != 1:
        val = (val * a) % p
        order += 1
        if order > p - 1:
            return None
    return order


def ex2():
    primes = [3, 7, 11]
    for p in primes:
        print(f"\n=== GF({p}) ===")
        for a in range(1, p):
            print(f"rząd({a}) = {mult_order(a, p)}")


def primitive_elements(p: int) -> list[int]:
    return [a for a in range(1, p) if mult_order(a, p) == p - 1]


def ex3():
    primes = [3, 5, 7]
    print(f"\nElementy pierwotne:")
    for p in primes:
        prim = primitive_elements(p)
        print(f"GF({p}) -> {prim}")


if __name__ == "__main__":
    ex1()
    ex2()
    ex3()