from werkzeug.security import generate_password_hash


def hash_password(plaintext_password):
    return generate_password_hash(plaintext_password)


if __name__ == "__main__":
    password = input("Enter password to hash: ")
    print("Hashed Password:", hash_password(password))
