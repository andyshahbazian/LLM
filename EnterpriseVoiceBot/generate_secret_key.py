# run this first before launching the app via: python generate_secret_key.py

import secrets
import os


def generate_secret_key():
    return secrets.token_hex(16)


def update_env_file(env_file_path, key_name, secret_key):
    new_lines = []
    key_found = False

    with open(env_file_path, 'r') as file:
        for line in file:
            if line.startswith(key_name):
                new_lines.append(f"{key_name}={secret_key}\n")
                key_found = True
            else:
                new_lines.append(line)

    if not key_found:
        new_lines.append(f"{key_name}={secret_key}\n")

    with open(env_file_path, 'w') as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    secret_key = generate_secret_key()
    update_env_file(".env", "FLASK_SECRET_KEY", secret_key)
    print("Secret key generated and updated in .env file.")
