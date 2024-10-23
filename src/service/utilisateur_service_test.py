import unittest
from unittest.mock import MagicMock
from business_object.users.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService


class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        self.utilisateurDao = MagicMock()  # Mock du DAO
        self.utilisateur_service = UtilisateurService(self.utilisateurDao)  # Service à tester

    def test_creer_compte(self):
        # Given
        pseudo = "test_user"
        nom = "Test User"
        mail = "test@example.com"
        ddn = "2000-01-01"
        mdp = "secure_password"
        administrateur = False
        organisateur = False

        # When
        utilisateur = self.utilisateur_service.creer_compte(
            pseudo, nom, mail, ddn, mdp, administrateur, organisateur
        )

        # Then
        self.utilisateurDao.insert_utilisateur.assert_called_once_with(
            pseudo, nom, mail, ddn, mdp, administrateur, organisateur
        )
        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.pseudo, pseudo)
        self.assertEqual(utilisateur.nom, nom)
        self.assertEqual(utilisateur.mail, mail)
        self.assertEqual(utilisateur.date_de_naissance, ddn)
        self.assertEqual(utilisateur.mdp, mdp)
        self.assertEqual(utilisateur.administrateur, administrateur)
        self.assertEqual(utilisateur.organisateur, organisateur)

    def test_creer_compte_echec_insertion(self):
        # Given
        self.utilisateurDao.insert_utilisateur.side_effect = Exception("Insertion failed")

        # When / Then
        with self.assertRaises(Exception):
            self.utilisateur_service.creer_compte(
                "test_user",
                "Test User",
                "test@example.com",
                "2000-01-01",
                "secure_password",
                False,
                False,
            )

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

    def test_pseudo_existe(self):
        # Given
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = {"pseudo": "existing_user"}

        # When
        result = self.utilisateur_service.pseudo_existe("existing_user")

        # Then
        self.assertTrue(result)

    def test_pseudo_n_existe_pas(self):
        # Given
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = None

        # When
        result = self.utilisateur_service.pseudo_existe("new_user")

        # Then
        self.assertFalse(result)

    def test_gestion_exception(self):
        # Given
        self.utilisateurDao.get_utilisateur_by_parameters.side_effect = Exception("DB error")

        # When / Then
        with self.assertRaises(Exception):
            self.utilisateur_service.pseudo_existe("any_user")


if __name__ == "__main__":
    unittest.main()
