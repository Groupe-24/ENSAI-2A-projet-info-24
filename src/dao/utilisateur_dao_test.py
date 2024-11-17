from utilisateur_dao import UtilisateurDAO
from pari_dao import ParisDAO
from db_connection import DBConnection
import hashlib
from uuid import uuid4

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
#     generate_unique_id("olivier"), "olivier", "olivierfdanel@gmail.com", "chips", None, True, False
# )
id_utilisateur = str(uuid4())
UtilisateurDAO().insert_utilisateur(
    "al",
    "RaphaelfBorny@gmail.com",
    "12",
    "ketchup",
    True,
    False,
    id_utilisateur,
    None,
)

# UtilisateurDAO().update_utilisateur(
#     UtilisateurDAO().get_utilisateur_by_parameters(pseudo="Raphael")[0]["id_utilisateur"],
#     organisateur=True,
# )


# print(UtilisateurDAO(DBConnection()).get_utilisateur_by_id(generate_unique_id("olivier")))


# print(UtilisateurDAO(DBConnection()).delete_utilisateur(generate_unique_id("Raphael")))

# print(UtilisateurDAO(DBConnection()).list_utilisateurs())
