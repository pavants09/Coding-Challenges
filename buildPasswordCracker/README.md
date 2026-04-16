# Password Cracker

A Python implementation of a password cracker demonstrating various cryptographic hashing techniques and cracking methods. This project is built as an educational tool to understand password security, hashing algorithms, and common vulnerabilities in password storage.

## Features

- **MD5 Hash Implementation**: Manual MD5 hash function implementation (with hashlib fallback for performance)
- **Brute Force Cracking**: Generates all possible permutations of passwords up to a specified length
- **Wordlist Cracking**: Uses a dictionary of common passwords for faster cracking
- **Rainbow Table**: Pre-computes hashes for common passwords and stores them for quick lookup
- **Multiple Hash Algorithms**: Support for MD5, SHA256, and salted hashing with PBKDF2
- **Salt Support**: Demonstrates secure password hashing with salting

## Requirements

- Python 3.x
- Standard library modules: `hashlib`, `itertools`, `string`, `json`, `os`

## Installation

1. Clone or download the repository
2. Ensure Python 3.x is installed
3. (Optional) Download a wordlist file (e.g., from CrackStation) and save it as `wordlist.txt`

## Usage

Run the script directly:

```bash
python password_cracker.py
```

### Functions

- `md5_hash(data)`: Compute MD5 hash of input string
- `brute_force_crack(target_hash, max_length=4, charset=string.ascii_letters + string.digits)`: Brute force crack MD5 hash
- `wordlist_crack(target_hash, wordlist_path)`: Crack using wordlist
- `build_rainbow_table(wordlist_path=None, max_length=4, charset=..., output_file='rainbow_table.json')`: Build rainbow table
- `rainbow_crack(target_hash, table_file='rainbow_table.json')`: Crack using rainbow table
- `sha256_hash(data)`: Compute SHA256 hash
- `salted_hash(password, salt)`: Compute salted hash using PBKDF2
- `crack_salted(target_hash, salt, wordlist_path)`: Crack salted hash

### Examples

```python
from password_cracker import md5_hash, brute_force_crack

# Hash a password
hash_value = md5_hash('password')
print(hash_value)  # 5f4dcc3b5aa765d61d8327deb882cf99

# Brute force crack
password = brute_force_crack('098f6bcd4621d373cade4e832627b4f6', max_length=4, charset='abcdefghijklmnopqrstuvwxyz')
print(password)  # test
```

## Configuration

- Adjust `max_length` for brute force and rainbow table generation
- Modify `charset` to include/exclude characters (e.g., add symbols for more complex passwords)
- Change salt and iterations in `salted_hash` for different security levels

## Disclaimer

This tool is for educational purposes only. Cracking passwords without authorization is illegal and unethical. Use this code to learn about password security and to build more secure systems, not to compromise others' accounts.

Always use strong, unique passwords and implement proper security measures like salting and key derivation functions in real applications.

## License

This project is for educational use only. No license is provided for unauthorized use.