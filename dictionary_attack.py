from hashing import verify_password

def dictionary_attack(hash_to_crack, wordlist):
    with open(wordlist, "r", errors="ignore") as f:
        for w in f:
            g = w.strip()
            if verify_password(g, hash_to_crack):
                return g
    return "Not Found"