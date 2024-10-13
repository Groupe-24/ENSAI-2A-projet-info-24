from utilisateur_dao import UtilisateurDAO
from db_connection import DBConnection
import hashlib

# pas des vrais tests mais permet de vérifier le fonctionnement du code


def generate_unique_id(data):
    # Vérifier si 'data' est une chaîne de caractères
    if isinstance(data, bytes):
        # Si data est déjà en 'bytes', pas besoin d'encoder
        return hashlib.sha256(data).hexdigest()
    else:
        # Sinon, on encode en 'utf-8' avant de générer le hachage
        return hashlib.sha256(data.encode("utf-8")).hexdigest()


# UtilisateurDAO(DBConnection()).insert_utilisateur(
#     generate_unique_id("olivier"), "olivier", "olivierfdanel@gmail.com", "chips", None, False
# )

# UtilisateurDAO(DBConnection()).insert_utilisateur(
#     generate_unique_id("Raphael"), "Raphael", "RaphaelfBorny@gmail.com", "ketchup", None, False
# )

# print(UtilisateurDAO(DBConnection()).get_utilisateur_by_id(generate_unique_id("olivier")))


print(UtilisateurDAO(DBConnection()).delete_utilisateur(generate_unique_id("Raphael")))

print(UtilisateurDAO(DBConnection()).list_utilisateurs())
