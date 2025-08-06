from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# pip install cryptography

# 📌 Nom de l'utilisateur
username = "user1"
# username = "user1_faux"
# username = "user1_fake"

# 📁 Noms des fichiers à générer
private_key_file = f"{username}_private.pem"
public_key_file = f"{username}_public.pem"

# ✅ 1. Générer la clé privée RSA (2048 bits minimum)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048  # Ou 4096 pour plus de sécurité
)

# ✅ 2. Extraire la clé publique à partir de la clé privée
public_key = private_key.public_key()

# ✅ 3. Sauvegarder la clé privée dans un fichier PEM
with open(private_key_file, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # ou PKCS8
        encryption_algorithm=serialization.NoEncryption()  # ⚠️ pas de mot de passe ici
    ))

# ✅ 4. Sauvegarder la clé publique dans un fichier PEM
with open(public_key_file, "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print(f"🔐 Clé privée enregistrée : {private_key_file}")
print(f"🔓 Clé publique enregistrée : {public_key_file}")
