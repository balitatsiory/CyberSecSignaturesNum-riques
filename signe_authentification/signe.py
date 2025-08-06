import os
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding



"""générer une empreinte numérique unique avec ta clé privée, qui permet à d'autres :

de vérifier que le document est authentique

de s’assurer qu’il n’a pas été modifié
   """
def signer_document(document_path, private_key_path, user):
    # Lire le document
    with open(document_path, 'rb') as f:
        contenu = f.read()

    # Calculer le hash SHA-256
    digest = hashes.Hash(hashes.SHA256())
    digest.update(contenu)
    hash_value = digest.finalize()

    # Charger la clé privée
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Signer le hash
    signature = private_key.sign(
        hash_value,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 🕒 Générer timestamp pour le nom du dossier
    now = datetime.utcnow().replace(microsecond=0)
    timestamp_str = now.isoformat().replace(":", "-") + "Z"
    output_dir = f"{user}_{timestamp_str}"

    # 📁 Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Chemins des fichiers à créer dans ce dossier
    base_filename = os.path.splitext(os.path.basename(document_path))[0]
    sig_path = os.path.join(output_dir, f"{base_filename}.sig")
    json_path = os.path.join(output_dir, f"{base_filename}.json")

    # Sauvegarder la signature (.sig) (signature electronique)
    with open(sig_path, 'wb') as f:
        f.write(signature)

    # Sauvegarder les métadonnées (.json) (métadonnées)
    metadata = {
        "user": user,
        "timestamp": now.isoformat() + "Z",
        "signature": base64.b64encode(signature).decode()
    }

    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Signature enregistrée dans : {output_dir}/")


if __name__ == '__main__':
    signer_document(document_path="D:/L4/cybersecurite/05_cryptographie/TP_Signatures/signe_authentification/document.txt",
                  #   private_key_path="D:/L4/cybersecurite/05_cryptographie/TP_Signatures/generer_cles/user1_private.pem",
                    private_key_path="D:/L4/cybersecurite/05_cryptographie/TP_Signatures/generer_cles/user1_faux_private.pem",
                    user="user1")
    
   #  mila sokafana anaty visual manokana amzay tsy miparitaka le dossier
