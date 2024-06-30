from werkzeug.security import generate_password_hash

# Function to hash a password
def hash_password(plaintext_password):
    return generate_password_hash(plaintext_password)

# Example usage
if __name__ == "__main__":
    password = input("Enter password to hash: ")
    print("Hashed Password:", hash_password(password))
