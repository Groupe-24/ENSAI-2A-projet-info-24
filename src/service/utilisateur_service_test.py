import unittest
from unittest.mock import MagicMock
from service.utilisateur_service import UtilisateurService
from business_object.users.utilisateur import Utilisateur


class TestUtilisateurService(unittest.TestCase):

    def setUp(self):
        # Create a mock for UtilisateurDAO
        self.mock_utilisateurDao = MagicMock()

        # Initialize UtilisateurService with the mock UtilisateurDAO
        self.utilisateur_service = UtilisateurService(self.mock_utilisateurDao)

    def test_creer_compte(self):
        # Set up the expected inputs and outputs
        pseudo = "user123"
        nom = "User"
        mail = "user@example.com"
        ddn = "1995-05-01"
        mdp = "password"

        # Call creer_compte
        utilisateur = self.utilisateur_service.creer_compte(pseudo, nom, mail, ddn, mdp)

        # Verify that the DAO's insert_utilisateur method was called with the correct parameters
        self.mock_utilisateurDao.insert_utilisateur.assert_called_once_with(
            pseudo, nom, mail, ddn, mdp
        )

        # Assert that the returned object is an instance of Utilisateur
        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.pseudo, pseudo)
        self.assertEqual(utilisateur.nom, nom)
        self.assertEqual(utilisateur.mail, mail)
        self.assertEqual(utilisateur.date_de_naissance, ddn)
        self.assertEqual(utilisateur.mdp, mdp)

    def test_se_connecter_utilisateur(self):
        # Set up the expected inputs and outputs
        pseudo = "user123"
        mdp = "password"
        mock_user = MagicMock(pseudo=pseudo, mdp=mdp)

        # Mock the return value of get_utilisateur_by_id
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user

        # Call se_connecter_utilisateur
        result = self.utilisateur_service.se_connecter_utilisateur(pseudo, mdp)

        # Verify that the DAO's get_utilisateur_by_id method was called with the correct parameter
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)

        # Assert that the login was successful
        self.assertTrue(result)

    def test_supprimer_utilisateur(self):
        # Set up the expected input
        pseudo = "user123"
        utilisateur = MagicMock(pseudo=pseudo)

        # Call supprimer_utilisateur
        self.utilisateur_service.supprimer_utilisateur(utilisateur)

        # Verify that the DAO's delete_utilisateur method was called with the correct parameter
        self.mock_utilisateurDao.delete_utilisateur.assert_called_once_with(pseudo)

    def test_se_connecter_administrateur(self):
        # Set up the expected inputs and outputs
        pseudo = "admin123"
        mdp = "adminpassword"
        mock_admin = MagicMock(pseudo=pseudo, mdp=mdp, administrateur=True)

        # Mock the return value of get_utilisateur_by_id
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_admin

        # Call se_connecter_administrateur
        result = self.utilisateur_service.se_connecter_administrateur(pseudo, mdp)

        # Verify that the DAO's get_utilisateur_by_id method was called
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)

        # Assert that the login as administrator was successful
        self.assertTrue(result)

    def test_se_connecter_organisateur(self):
        # Set up the expected inputs and outputs
        pseudo = "organizer123"
        mdp = "organizerpassword"
        mock_organizer = MagicMock(pseudo=pseudo, mdp=mdp, organisateur=True)

        # Mock the return value of get_utilisateur_by_id
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_organizer

        # Call se_connecter_organisateur
        result = self.utilisateur_service.se_connecter_organisateur(pseudo, mdp)

        # Verify that the DAO's get_utilisateur_by_id method was called
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)

        # Assert that the login as organizer was successful
        self.assertTrue(result)

    def test_connection_ok(self):
        # Set up test data
        pseudo = "user123"
        mdp = "password"
        mock_user = MagicMock(pseudo=pseudo, mdp=mdp)
        mock_admin = MagicMock(pseudo=pseudo, mdp=mdp, administrateur=True)
        mock_organizer = MagicMock(pseudo=pseudo, mdp=mdp, organisateur=True)

        # Test for normal user login
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)

        # Test for administrator login
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_admin
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)

        # Test for organizer login
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_organizer
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)

        # Test for failed login (user does not exist)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = None
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertFalse(result)

        # Test for failed login (incorrect password)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user
        mock_user.mdp = "wrongpassword"
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
