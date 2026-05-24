import optparse

# Brute-force attack: try all 26 keys
def attack(msg):
    print("[>_> <-< <_< ^_^] Starting brute-force attack...")

    for key in range(26):  # Try every possible Caesar shift
        result = ""

        for char in msg:
            if char.isalpha():
                if char.isupper():
                    shift = 65
                else:
                    shift = 97
                #reverse order shift
                position = ord(char) - shift
                new_position = (position - key) % 26
                new_char = chr(new_position + shift)
                #update
                result += new_char
            else: #leave space unchanged
                result += char

        print(f"Key {key:2d}: {result}")


def main():
    parser = optparse.OptionParser("usage%prog -m <message>")
    parser.add_option('-m', dest='msg', type='string',
                      help='encrypted message to attack')

    (options, args) = parser.parse_args()
    msg = options.msg

    if msg == None:
        print("[0_0] You must specify an encrypted message with -m")
        exit(0)

    attack(msg)


if __name__ == "__main__":
    main()