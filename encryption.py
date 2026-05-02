import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes



#key Derivation
def derive_key(password,salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32, salt=salt,iterations=100000)
    return kdf.derive(password.encode())


# 🔒 Encrypt function
def encrypt_message(message, key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(message.encode()) + encryptor.finalize()

    return base64.b64encode(iv + encrypted).decode()


# 🔓 Decrypt function
def decrypt_message(encrypted_message, key):
    data = base64.b64decode(encrypted_message)

    iv = data[:16]
    encrypted = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return decrypted.decode()


