from utilisateur_dao import UtilisateurDAO
from db_connection import DBConnection
import hashlib


UtilisateurDAO().insert_utilisateur(
    pseudo="Olivier",
    email="olivierfdanel@gmail.com",
    password="Olivier2307",
    administrateur=True,
    organisateur=True,
)
