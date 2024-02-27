from typing import Union, Tuple
# from flask import Flask, render_template

def f(x: float) -> float:
    return ((x + 1) % 2) - 1

def normalizeASCII(x: float) -> float:
    return (x - 127.5) / 127.5

def denormalizeASCII(x: float) -> float:
    return (x * 127.5) + 127.5

def KeyGeneration(length16key, c1, c2, y1, y2):
    listOfKey = []
    lasttwo = []
    tempvalue = 0
    for i in range(16):
        if(i == 0):
            tempvalue = ord(length16key[i]) + (c1 * y1) + (c2 * y2)
            listOfKey.append(tempvalue%2 - 1)
        elif(i == 1):
            tempvalue = ord(length16key[i]) + (c1 * listOfKey[i-1]) + (c2 * y1)
            listOfKey.append(tempvalue%2 - 1)
        elif(i > 1):
            tempvalue = ord(length16key[i]) + (c1 * listOfKey[i-1]) + (c2 * listOfKey[i-2])
            listOfKey.append(tempvalue%2 - 1)
    lasttwo.append(listOfKey[14])
    lasttwo.append(listOfKey[15])
    return lasttwo

def encrypt_char(plain_char: str, c1: float, c2: float, y_minus_1: float, y_minus_2: float) -> Tuple[str, float, float]:
    last = y_minus_1
    second_last = y_minus_2

    decrypt_last = last
    decrypt_second_last = second_last

    encrypted = f(normalizeASCII(ord(plain_char)) + c1 * last + c2 * second_last)
    denormalized = denormalizeASCII(encrypted)
    while True:
            # print("Int of denormalized: ", int(denormalized))
            tmp_cipher_text = chr(int(denormalized))
            decrypted_character, tmp_decrypt_last, tmp_decrypt_second_last = decrypted_char(tmp_cipher_text, c1, c2, decrypt_last, decrypt_second_last)
            denormalized += ord(plain_char) - ord(decrypted_character)
            # print(c, decrypted_char)
            if ord(plain_char) - ord(decrypted_character) == 0:
                break
    # get the last two value of the iteration
    decrypt_last = tmp_decrypt_last
    decrypt_second_last = tmp_decrypt_second_last    
    
    # get  the encrypted text
    cipher_char = chr(int(denormalized))
    second_last = decrypt_second_last
    last = decrypt_last
    return cipher_char, last, second_last

def decrypted_char(cipher_char: str, c1: float, c2: float, y_minus_1: float, y_minus_2: float) -> Tuple[str, float, float]:
    last = y_minus_1
    second_last = y_minus_2

    normalized = normalizeASCII(ord(cipher_char))
    decrypted = f(normalized - c1 * last - c2 * second_last)
    plain_char = chr(int(denormalizeASCII(decrypted)))
    second_last = last
    last = normalized
    return plain_char, last, second_last


def encrypt_text(plain_text: str, c1: float, c2: float, y_minus_1: float, y_minus_2: float) -> str:
    if len(plain_text) == 0:
        raise Exception("Plain text length must be greater than 0")
    cipher_text = ""
    last = y_minus_1
    second_last = y_minus_2

    # print(len(plain_text))
    for i in range(len(plain_text)):
        c = plain_text[i]
        encrypted_char, last, second_last = encrypt_char(c, c1, c2, last, second_last)
        cipher_text += encrypted_char
    print(cipher_text)
    return cipher_text

def decrypt_text(cipher_text: str, c1: float, c2: float, y_minus_1: float, y_minus_2: float) -> Tuple[str, float, float]:
    if len(cipher_text) == 0:
        raise Exception("Cipher text length must be greater than 0")

    plain_text = ""
    last = y_minus_1
    second_last = y_minus_2

    # real_plain_text_len = 10
    for i in range(len(cipher_text)):
        plain_char, last, second_last = decrypted_char(cipher_text[i], c1, c2, last, second_last)
        plain_text += plain_char
    return plain_text


# length16key = "ChhorngKy1234JOL"
# plaintext = "Hi"

# y1 = 0.433
# y2 = -0.133

# # Manually pick c1 and c2 much be within the triangle
# c1 = 0.12
# c2 = -0.1

# Store all of iteration value
# lastTwoC = KeyGeneration(length16key, c1, c2, y1, y2)
# c1prime = lastTwoC[0]
# c2prime = lastTwoC[1]
# print(c1prime, c2prime)
# # store encryption text
# cypher_text = encrypt_text(plaintext, c1prime, c2prime, y1, y2)
# decryptext = decrypt_text(cypher_text, c1prime, c2prime, y1, y2)
# print ("Plain Text: ", plaintext)
# print("Length Plaint: ", len(plaintext))
# print("Encrypted Text: ")
# print(cypher_text)
# print("Length cypher: ", len(cypher_text))
# print("Decrypted Text: ")
# print(decryptext)
# print("Length decrypt: ", len(decryptext))



# app = Flask(__name__)

# @app.route('/')
# def index():
#     name = {
#         "cyphertext" : cypher_text,
#         "age" : 200
#     }
#     return render_template('main.html', data=name)

# if __name__ == "__main__":
#     app.run(debug=True)