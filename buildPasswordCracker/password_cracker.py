import hashlib
import itertools
import string
import json
import os
from hashlib import pbkdf2_hmac

# MD5 Implementation (from scratch)
class MD5:
    def __init__(self):
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
        self.K = [0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE,
                  0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
                  0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE,
                  0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
                  0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
                  0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
                  0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
                  0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
                  0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C,
                  0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
                  0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
                  0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
                  0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039,
                  0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
                  0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
                  0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391]

    def left_rotate(self, value, amount):
        return ((value << amount) | (value >> (32 - amount))) & 0xFFFFFFFF

    def F(self, x, y, z): return (x & y) | (~x & z)
    def G(self, x, y, z): return (x & z) | (y & ~z)
    def H(self, x, y, z): return x ^ y ^ z
    def I(self, x, y, z): return y ^ (x | ~z)

    def process_chunk(self, chunk):
        w = [0] * 16
        for i in range(16):
            w[i] = int.from_bytes(chunk[i*4:(i+1)*4], 'little')

        a, b, c, d = self.A, self.B, self.C, self.D

        for i in range(64):
            if i < 16:
                f = self.F(b, c, d)
                g = i
            elif i < 32:
                f = self.G(b, c, d)
                g = (5*i + 1) % 16
            elif i < 48:
                f = self.H(b, c, d)
                g = (3*i + 5) % 16
            else:
                f = self.I(b, c, d)
                g = (7*i) % 16

            f = (f + a + self.K[i] + w[g]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + self.left_rotate(f, self.s[i])) & 0xFFFFFFFF

        self.A = (self.A + a) & 0xFFFFFFFF
        self.B = (self.B + b) & 0xFFFFFFFF
        self.C = (self.C + c) & 0xFFFFFFFF
        self.D = (self.D + d) & 0xFFFFFFFF

    def update(self, message):
        message = bytearray(message)
        msg_len = len(message) * 8
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += msg_len.to_bytes(8, 'little')

        for i in range(0, len(message), 64):
            self.process_chunk(message[i:i+64])

    def digest(self):
        return (self.A.to_bytes(4, 'little') +
                self.B.to_bytes(4, 'little') +
                self.C.to_bytes(4, 'little') +
                self.D.to_bytes(4, 'little'))

    def hexdigest(self):
        return self.digest().hex()

def md5_hash(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

# Brute force cracker
def brute_force_crack(target_hash, max_length=4, charset=string.ascii_letters + string.digits):
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            password = ''.join(combo)
            if md5_hash(password) == target_hash:
                return password
    return None

# Word list cracker
def wordlist_crack(target_hash, wordlist_path):
    with open(wordlist_path, 'r') as f:
        for line in f:
            password = line.strip()
            if md5_hash(password) == target_hash:
                return password
    return None

# Build rainbow table
def build_rainbow_table(wordlist_path=None, max_length=4, charset=string.ascii_letters + string.digits, output_file='rainbow_table.json'):
    table = {}
    if wordlist_path:
        with open(wordlist_path, 'r') as f:
            for line in f:
                password = line.strip()
                table[md5_hash(password)] = password
    else:
        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                table[md5_hash(password)] = password
    with open(output_file, 'w') as f:
        json.dump(table, f)

# Crack using rainbow table
def rainbow_crack(target_hash, table_file='rainbow_table.json'):
    if not os.path.exists(table_file):
        return None
    with open(table_file, 'r') as f:
        table = json.load(f)
    return table.get(target_hash)

# Other hashes and salting
def sha256_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def salted_hash(password, salt):
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

def crack_salted(target_hash, salt, wordlist_path):
    with open(wordlist_path, 'r') as f:
        for line in f:
            password = line.strip()
            if salted_hash(password, salt) == target_hash:
                return password
    return None

# Main function
if __name__ == "__main__":
    # Test MD5
    print("MD5 of 'password':", md5_hash('password'))

    # Brute force test
    test_hashes = ['098f6bcd4621d373cade4e832627b4f6', 'b5c0b187fe309af0f4d35982fd961d7e']  # for 'test' and 'love'
    for h in test_hashes:
        result = brute_force_crack(h, max_length=4, charset=string.ascii_lowercase)
        print(f"Brute force crack for {h}: {result}")

    # Word list crack (assuming wordlist.txt exists)
    wordlist_hash = '2bdb742fc3d075ec6b73ea414f27819a'
    if os.path.exists('wordlist.txt'):
        result = wordlist_crack(wordlist_hash, 'wordlist.txt')
        print(f"Wordlist crack for {wordlist_hash}: {result}")
    else:
        print("Wordlist not found, skipping wordlist crack")

    # Build rainbow table
    build_rainbow_table(max_length=4)

    # Rainbow crack
    result = rainbow_crack(wordlist_hash)
    print(f"Rainbow crack for {wordlist_hash}: {result}")

    # SHA256 example
    print("SHA256 of 'password':", sha256_hash('password'))

    # Salted example
    salt = 'randomsalt'
    salted = salted_hash('password', salt)
    print(f"Salted hash: {salted}")
    if os.path.exists('wordlist.txt'):
        result = crack_salted(salted, salt, 'wordlist.txt')
        print(f"Crack salted: {result}")
    else:
        print("Wordlist not found, skipping salted crack")