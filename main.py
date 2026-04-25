import hashlib
import os
from passlib.context import CryptContext
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# Encryption (AES)
def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_message).decode()

def decrypt_message(encrypted_message, key):
    data = base64.b64decode(encrypted_message)
    iv = data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(data[16:]) + decryptor.finalize()).decode()

# Generate Key for AES
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Strong Password Policy
def check_password_policy(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must include at least one number."
    if not any(char.isupper() for char in password):
        return "Password must include at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must include at least one lowercase letter."
    if not any(char in "!@#$%^&*()_+" for char in password):
        return "Password must include at least one special character."
    return "Password is strong."

# Brute Force Example
from itertools import product
import string

def brute_force_password(hash_to_crack, charset, max_length):
    for length in range(1, max_length + 1):
        for attempt in product(charset, repeat=length):
            attempt_password = ''.join(attempt)
            if verify_password(attempt_password, hash_to_crack):
                return attempt_password
    return None

# Example Usage
if __name__ == "__main__":
    # Hashing example
    password = "Secure@123"
    hashed_password = hash_password(password)
    print("Original Password:", password)
    print("Hashed Password:", hashed_password)

    # Verify password
    print("Password Verified:", verify_password(password, hashed_password))

    # Password policy check
    policy_message = check_password_policy(password)
    print("Password Policy:", policy_message)

    # Encryption example
    salt = os.urandom(16)
    key = derive_key(password, salt)
    message = "Sensitive Data"
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    print("Original Message:", message)
    print("Encrypted Message:", encrypted)
    print("Decrypted Message:", decrypted)

    # Brute force example
    charset = string.ascii_letters + string.digits
    cracked_password = brute_force_password(hashed_password, charset, 6)
    print("Cracked Password:", cracked_password)
