from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to a file
with open("memory/secret.key", "wb") as key_file:
    key_file.write(key)

print("Key generated and saved to memory/secret.key ✅")
