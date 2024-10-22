import unittest
from unittest.mock import MagicMock
from service.utilisateur_service import UtilisateurService
from business_object.users.utilisateur import Utilisateur


class TestUtilisateurService(unittest.TestCase):

    def setUp(self):
        self.mock_utilisateurDao = MagicMock()
        self.utilisateur_service = UtilisateurService(self.mock_utilisateurDao)

    def test_creer_compte(self):
        pseudo = "user123"
        nom = "User"
        mail = "user@example.com"
        ddn = "1995-05-01"
        mdp = "password"
        utilisateur = self.utilisateur_service.creer_compte(pseudo, nom, mail, ddn, mdp)
        self.mock_utilisateurDao.insert_utilisateur.assert_called_once_with(
            pseudo, nom, mail, ddn, mdp
        )
        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.pseudo, pseudo)
        self.assertEqual(utilisateur.nom, nom)
        self.assertEqual(utilisateur.mail, mail)
        self.assertEqual(utilisateur.date_de_naissance, ddn)
        self.assertEqual(utilisateur.mdp, mdp)

    def test_se_connecter_utilisateur(self):
        pseudo = "user123"
        mdp = "password"
        mock_user = MagicMock(pseudo=pseudo, mdp=mdp)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user
        result = self.utilisateur_service.se_connecter_utilisateur(pseudo, mdp)
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)
        self.assertTrue(result)

    def test_supprimer_utilisateur(self):
        pseudo = "user123"
        utilisateur = MagicMock(pseudo=pseudo)
        self.utilisateur_service.supprimer_utilisateur(utilisateur)
        self.mock_utilisateurDao.delete_utilisateur.assert_called_once_with(pseudo)

    def test_se_connecter_administrateur(self):
        pseudo = "admin123"
        mdp = "adminpassword"
        mock_admin = MagicMock(pseudo=pseudo, mdp=mdp, administrateur=True)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_admin
        result = self.utilisateur_service.se_connecter_administrateur(pseudo, mdp)
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)
        self.assertTrue(result)

    def test_se_connecter_organisateur(self):
        pseudo = "organizer123"
        mdp = "organizerpassword"
        mock_organizer = MagicMock(pseudo=pseudo, mdp=mdp, organisateur=True)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_organizer
        result = self.utilisateur_service.se_connecter_organisateur(pseudo, mdp)
        self.mock_utilisateurDao.get_utilisateur_by_id.assert_called_once_with(pseudo)
        self.assertTrue(result)

    def test_connection_ok(self):
        pseudo = "user123"
        mdp = "password"
        mock_user = MagicMock(pseudo=pseudo, mdp=mdp)
        mock_admin = MagicMock(pseudo=pseudo, mdp=mdp, administrateur=True)
        mock_organizer = MagicMock(pseudo=pseudo, mdp=mdp, organisateur=True)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_admin
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_organizer
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertTrue(result)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = None
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertFalse(result)
        self.mock_utilisateurDao.get_utilisateur_by_id.return_value = mock_user
        mock_user.mdp = "wrongpassword"
        result = self.utilisateur_service.connection_ok(pseudo, mdp)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
