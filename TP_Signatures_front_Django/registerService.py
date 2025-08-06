import json
import os

REGISTRE_PATH = 'registres/public_keys.json'

def load_register():
    if os.path.exists(REGISTRE_PATH):
        with open(REGISTRE_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_register(data):
    with open(REGISTRE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def register_user(username, public_key_pem):
    registre = load_register()
    registre[username] = public_key_pem
    save_register(registre)