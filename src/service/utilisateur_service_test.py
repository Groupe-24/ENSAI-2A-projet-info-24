import unittest
from unittest.mock import MagicMock
from business_object.users.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService


class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        self.utilisateurDao = MagicMock()  # Mock du DAO
        self.utilisateur_service = UtilisateurService(self.utilisateurDao)  # Service à tester

    def test_creer_compte(self):
        """Test de la création de compte utilisateur"""
        # GIVEN
        pseudo = "testUser"
        nom = "Test"
        mail = "test@mail.com"
        ddn = "01/01/1990"
        mdp = "password123"

        # WHEN
        utilisateur = self.utilisateur_service.creer_compte(pseudo, nom, mail, ddn, mdp)

        # THEN
        self.utilisateurDao.insert_utilisateur.assert_called_with(pseudo, nom, mail, ddn, mdp)
        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.pseudo, pseudo)
        self.assertEqual(utilisateur.nom, nom)

    def test_se_connecter_utilisateur_succes(self):
        """Test de connexion réussie d'un utilisateur"""
        # GIVEN
        pseudo = "testUser"
        mdp = "password123"
        mock_user = [{"pseudo": pseudo, "password": mdp}]  # Simule un utilisateur dans la BD
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = mock_user

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur(pseudo, mdp)

        # THEN
        self.utilisateurDao.get_utilisateur_by_parameters.assert_called_with(pseudo=pseudo)
        self.assertTrue(result)

    def test_se_connecter_utilisateur_echec(self):
        """Test de connexion échouée d'un utilisateur (mauvais mot de passe)"""
        # GIVEN
        pseudo = "testUser"
        mdp = "wrongPassword"
        mock_user = [
            {"pseudo": pseudo, "password": "password123"}
        ]  # Simule un utilisateur dans la BD
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = mock_user

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur(pseudo, mdp)

        # THEN
        self.assertFalse(result)

    def test_se_connecter_utilisateur_non_existant(self):
        """Test de connexion échouée avec un utilisateur non existant"""
        # GIVEN
        pseudo = "nonExistantUser"
        mdp = "password123"
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = (
            []
        )  # Aucun utilisateur trouvé

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur(pseudo, mdp)

        # THEN
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
