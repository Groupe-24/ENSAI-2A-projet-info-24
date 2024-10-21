# Fichier avec des fonctions génériques utiles


# Générer un identifiant unique basé sur une chaîne


def generate_unique_id(data):
    # Vérifier si 'data' est une chaîne de caractères
    if isinstance(data, bytes):
        # Si data est déjà en 'bytes', pas besoin d'encoder
        return hashlib.sha256(data).hexdigest()
    else:
        # Sinon, on encode en 'utf-8' avant de générer le hachage
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
