
from hashing import hash_password, verify_password
from policy import password_policy
from encryption import derive_key, encrypt_message, decrypt_message
from bruteforce import brute_force_simple
from dictionary_attack import dict_attack
import os

def main():
    print("===== CYBERSECURITY TOOLKIT =====\n")

    # 🔐 Step 1: Take password
    password = input("Enter a password: ")

    # 🔎 Step 2: Check Password Policy
    print("\n[+] Checking Password Strength...")
    print(password_policy(password))

    # 🔒 Step 3: Hash Password
    hashed = hash_password(password)
    print("\n[+] Hashed Password:", hashed)

    # 🔑 Step 4: Key Derivation
    salt = os.urandom(16)
    key = derive_key(password, salt)

    # 🔐 Step 5: Encrypt Message
    message = "Sensitive Data"
    encrypted = encrypt_message(message, key)
    print("\n[+] Encrypted Message:", encrypted)

    # 🔓 Step 6: Decrypt Message
    decrypted = decrypt_message(encrypted, key)
    print("[+] Decrypted Message:", decrypted)

    # 💣 Step 7: Brute Force Attack
    print("\n[!] Running Brute Force Attack...")
    charset = "abc123"
    cracked = brute_force_simple(hashed, charset, 4)
    print("Brute Force Result:", cracked)

    # 📚 Step 8: Dictionary Attack
    print("\n[!] Running Dictionary Attack...")
    dict_result = dict_attack(hashed, "wordlist.txt")
    print("Dictionary Attack Result:", dict_result)


if __name__ == "__main__":
    main()