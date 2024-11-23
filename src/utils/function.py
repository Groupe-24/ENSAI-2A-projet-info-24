import hashlib

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


def generer_hash(chaine, algorithme="sha256"):
    """
    Génère le hash d'une chaîne en utilisant un algorithme de hashage spécifié.

    Args:
        chaine (str): La chaîne à hasher.
        algorithme (str): Le nom de l'algorithme (par défaut, "sha256").
                          Options courantes : "md5", "sha1", "sha256", "sha512".

    Returns:
        str: Le hash hexadécimal de la chaîne.
    """
    try:
        # Obtenir l'objet de hashage pour l'algorithme spécifié
        h = hashlib.new(algorithme)
        # Encoder la chaîne en bytes et calculer le hash
        h.update(chaine.encode("utf-8"))
        # Retourner le hash sous forme hexadécimale
        return h.hexdigest()
    except ValueError:
        return f"Algorithme de hashage '{algorithme}' non supporté."
