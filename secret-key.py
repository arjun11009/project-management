import secrets

# Generate a secure random key
secret_key = secrets.token_hex(32)
print(f"Your secure SECRET_KEY: {secret_key}")