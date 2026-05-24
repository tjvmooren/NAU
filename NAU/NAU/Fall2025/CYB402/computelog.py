import argparse

def discrete_log(p, a, b):

    for x in range(p - 1):  # search 1, ..., p-1
        if pow(a, x, p) == b:
            return x

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("p", type = int)
    parser.add_argument("a", type = int)
    parser.add_argument("b", type = int)
    args = parser.parse_args()

    x = discrete_log(args.p, args.a, args.b)
    if x != None:
        print("Solution: x =", x)
    else:
        print("No solution found in Z*_p.")