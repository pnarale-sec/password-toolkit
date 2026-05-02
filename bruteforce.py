from itertools import product
from hashing import verify_password   # ✅ IMPORTANT

def brute_force_simple(hash_to_crack, charset, max_length):
    for length in range(1, max_length + 1):
        for combo in product(charset, repeat=length):
            guess = "".join(combo)

            if verify_password(guess, hash_to_crack):
                return guess

    return "Not Found"
