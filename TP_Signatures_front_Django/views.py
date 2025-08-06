from django.http import HttpResponse
from django.shortcuts import render
from .forms import PublicKeyUploadForm
from .registerService import register_user
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from .registerService import load_register  # Assure-toi d’avoir cette fonction


def register_view(request):
    if request.method == 'POST':
        form = PublicKeyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            public_key = request.FILES['public_key_file'].read().decode()
            register_user(username, public_key)
            return HttpResponse("✅ Utilisateur enregistré.")
    else:
        form = PublicKeyUploadForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return HttpResponse("<h1>Bienvenue dans l'application de signature électronique !</h1>")

def verify_signature_view(request):
    message = None

    if request.method == 'POST':
        document_file = request.FILES.get('document')
        signature_file = request.FILES.get('signature_json')

        if not document_file or not signature_file:
            message = "❌ Veuillez fournir les deux fichiers."
        else:
            try:
                # Lire le contenu du fichier texte
                document_content = document_file.read()

                # Lire le contenu du JSON
                signature_data = json.loads(signature_file.read().decode())

                # Extraire les données
                user = signature_data["user"]
                signature_b64 = signature_data["signature"]
                signature = base64.b64decode(signature_b64)

                # Recalculer le hash du document
                digest = hashes.Hash(hashes.SHA256())
                digest.update(document_content)
                hash_value = digest.finalize()

                # Charger la clé publique depuis le registre
                registre = load_register()
                public_key_pem = registre.get(user)

                if not public_key_pem:
                    message = f"❌ Utilisateur '{user}' non trouvé dans le registre."
                else:
                    public_key = serialization.load_pem_public_key(public_key_pem.encode())

                    # Vérification de la signature
                    public_key.verify(
                        signature,
                        hash_value,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    message = "✅ Signature valide."

            except InvalidSignature:
                message = "❌ Signature invalide."
            except Exception as e:
                message = f"❌ Erreur lors de la vérification : {str(e)}"

    return render(request, 'verify.html', {'message': message})