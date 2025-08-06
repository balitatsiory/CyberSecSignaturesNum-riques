# CyberSecSignaturesNum-riques
TP – Signatures numériques et Autorité de  Certification simulée

# lancement : 
python manage.py runserver

Signer un document = Créer une empreinte numérique avec sa clé privée, pour prouver l’authenticité et l’intégrité du fichier.

 # Objectif global : créer un système simple de signatures électroniques avec Django
 
🧠 Acteurs :
Rôle	Description
👤 Utilisateur	Il possède une clé privée RSA et signe des documents
🖥️ Application Django (serveur)	Elle enregistre les clés publiques, reçoit les signatures, et vérifie leur validité
🛡️ Autorité (fictive)	C’est le rôle de Django dans ce cas : il agit comme une autorité centrale qui garde les clés publiques dans un registre

🔐 SCÉNARIO 1 : Enregistrement de l'utilisateur et de sa clé publique
📍 But : s'assurer que l'application connaît la clé publique de chaque utilisateur.

Étapes :
L’utilisateur crée ses clés RSA avec un script ou logiciel :

user1_private.pem

user1_public.pem

Il va sur Django : /register/

Il remplit un formulaire avec son nom d'utilisateur et téléverse sa clé publique

✍️ SCÉNARIO 2 : Signature d’un document .txt (en local, côté utilisateur)
📍 But : permettre à l’utilisateur de signer un fichier texte avec sa clé privée

Étapes :
L’utilisateur a :

Un fichier texte document.txt

Sa clé privée user1_private.pem

Il lance un script Python local qui :

Lit document.txt

Calcule le hash SHA-256

Signe ce hash avec la clé privée

Produit :

document.sig (signature binaire)

document.json (avec signature + nom utilisateur + date)

🔎 SCÉNARIO 3 : Vérification de la signature (dans Django)
📍 But : vérifier si la signature correspond bien au fichier signé, via la clé publique de l’utilisateur.

Étapes :
L’utilisateur (ou un autre) téléverse :

document.txt

document.json

Django /verify/ :

Lit document.txt

Recalcule le hash SHA-256

Récupère la clé publique de user1 depuis public_keys.json

Vérifie si la signature est valide avec cette clé

✅ Résultat : Django affiche :

✅ "Signature valide"

❌ ou "Signature invalide"
