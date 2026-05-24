import optparse

# Takes in a plaintext message
# and an integer key and encrypts
# using the Caesar cipher approach
def encrypt(msg, key):
    result = ""

    #loop through each character of message
    for char in msg:
        if char.isalpha(): 
        #check upper vs lower
            if char.isupper():
                shift = 65 # 'A'
            else:
                shift = 97 # 'a'

            # Convert char -> number, shift, then convert back
            position = ord(char) - shift
            new_position = (position + key) % 26
            new_char = chr(new_position + shift)
            # update
            result += new_char
        
        else: #leave spaces unchanged
            result += char
            
    print("-_- Encrypted: ", result)
    return result

# Takes in an encrypted message
# and an integer key and decrypts
# using the Caesar cipher approach
def decrypt(msg, key):
    result = ""
    
    for char in msg:
        if char.isalpha():
            if char.isupper():
                shift = 65
            else:
                shift = 97

            #reverse order shift(subtract)
            position = ord(char) - shift
            new_position = (position - key) % 26
            new_char = chr(new_position + shift)
            #update
            result += new_char
        
        else:
            result += char

    print("_-_ Decrypted: ", result)
    return result


def main():
    parser = optparse.OptionParser("usage%prog "+ "-f <decrypt | encrypt> -m <message> -k <key>")
    parser.add_option('-f', dest='function', type='string', help='[ decrypt | encrypt ]')
    parser.add_option('-m', dest='msg', type='string',  help='message to encrypt (plaintext) or decrypt (encrypted)')
    parser.add_option('-k', dest='key', type='int', help='cipher key as an integer')
    (options, args) = parser.parse_args()
    function = options.function
    if ((function != "encrypt" and function != "decrypt") or function == None):
        print('[0_0] You must specify a valid function: "encrypt" or "decrypt"')
        exit(0)
    msg = str(options.msg)
    key = int(options.key)
    if (msg == None) | (key == None):
        print('[0_0] You must specify a message and key.')
        exit(0)
    if function == "encrypt":
        encrypt(msg, key)
    elif function == "decrypt":
        decrypt(msg, key)

if __name__ == '__main__':
    main()

