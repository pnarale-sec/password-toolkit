
def password_policy(password):
    if len(password)<8:
        return "password must be 8 character"
    if not any(char.isupper() for char in password):
        return "password must contain upper character"
    if not any(char.islower() for char in password):
        return "password must contain lower  char"
    if not any(char.isdigit() for char in password):
        return "password must contain digit character"
    if not any(char in "!@#$%^&*()_+" for char in password):
        return "Password must include at least one special character."
    
    return "Password is strong."