from cryptography.fernet import Fernet
import os
import json

KEY_FILE = "memory/secret.key"
MEMORY_FILE = "memory/memory.txt"

# Load the encryption key
def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Initialize the Fernet cipher
def get_cipher():
    key = load_key()
    return Fernet(key)

# Save a message (dict or string) to encrypted memory
def save_to_memory(message):
    cipher = get_cipher()
    encrypted = cipher.encrypt(json.dumps(message).encode())  # ✅ Convert to JSON then encode

    with open(MEMORY_FILE, "ab") as f:
        f.write(encrypted + b"\n")

# Load and decrypt all memory messages
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    cipher = get_cipher()
    messages = []

    with open(MEMORY_FILE, "rb") as f:
        for line in f:
            try:
                decrypted = json.loads(cipher.decrypt(line.strip()).decode())  # ✅ Convert from JSON
                messages.append(decrypted)
            except Exception:
                continue  # Skip unreadable lines

    return messages
# Search memory for related entries
def search_memory(query, limit=3):
    results = []
    query = query.lower()

    for item in load_memory():
        text = ""
        if isinstance(item, dict):
            text = json.dumps(item)
        elif isinstance(item, str):
            text = item

        if query in text.lower():
            results.append(text)

    return results[-limit:]  # Return last N matches
