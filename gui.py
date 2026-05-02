import tkinter as tk
from tkinter import messagebox
import os

from hashing import hash_password
from policy import password_policy
from encryption import derive_key, encrypt_message, decrypt_message
from bruteforce import brute_force_simple
from dictionary_attack import dict_attack

# Functions
def check_security():
    password = entry.get()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    # Policy
    policy = password_policy(password)

    # Hash
    hashed = hash_password(password)

    # Encryption
    salt = os.urandom(16)
    key = derive_key(password, salt)
    encrypted = encrypt_message("Sensitive Data", key)
    decrypted = decrypt_message(encrypted, key)

    output.delete(1.0, tk.END)
    output.insert(tk.END, f"Policy: {policy}\n\n")
    output.insert(tk.END, f"Hash:\n{hashed}\n\n")
    output.insert(tk.END, f"Encrypted:\n{encrypted}\n")
    output.insert(tk.END, f"Decrypted: {decrypted}\n")

def run_bruteforce():
    password = entry.get()
    hashed = hash_password(password)

    result = brute_force_simple(hashed, "abc123", 3)

    attack_output.delete(1.0, tk.END)
    attack_output.insert(tk.END, f"Brute Force Result: {result}")

def run_dictionary():
    password = entry.get()
    hashed = hash_password(password)

    result = dict_attack(hashed, "wordlist.txt")

    attack_output.delete(1.0, tk.END)
    attack_output.insert(tk.END, f"Dictionary Result: {result}")

# UI
root = tk.Tk()
root.title("Cybersecurity Toolkit")
root.geometry("600x600")

title = tk.Label(root, text="Cybersecurity Toolkit", font=("Arial", 18, "bold"))
title.pack(pady=10)

entry = tk.Entry(root, show="*", width=30)
entry.pack(pady=5)

btn_check = tk.Button(root, text="Check Security", command=check_security)
btn_check.pack(pady=5)

output = tk.Text(root, height=10, width=70)
output.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

btn_brute = tk.Button(frame, text="Brute Force", command=run_bruteforce)
btn_brute.grid(row=0, column=0, padx=10)

btn_dict = tk.Button(frame, text="Dictionary Attack", command=run_dictionary)
btn_dict.grid(row=0, column=1, padx=10)

attack_output = tk.Text(root, height=8, width=70)
attack_output.pack(pady=10)

root.mainloop()