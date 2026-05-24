# return true if a is a generator of the group Z*_p.
# compute all powers a^k mod p and get all p-1 elements.

def is_generator(a, p):
    testlist = set()

    # need exponents 1...(p-1)
    for exp in range(1, p):
        testgen = pow(a, exp, p)
        testlist.add(testgen)

    return len(testlist) == p - 1 

# test every a in {1, ..., p-1},
# then return list of all generators
def generator_list(p):
    gens = []
    for a in range(1, p):  # elements of Z*_p are 1..p-1
        if is_generator(a, p):
            gens.append(a)
    return gens


# get the prime from da user
if __name__ == "__main__":
    p = int(input("Enter a prime p: "))
    gens = generator_list(p)
    print(f"Generators of Z*_{p}:")
    print(gens)
    print("Number of generators:", len(gens))