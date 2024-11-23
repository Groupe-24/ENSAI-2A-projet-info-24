import unittest
from unittest.mock import MagicMock
from business_object.users.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService


class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        self.utilisateurDao = MagicMock()
        self.utilisateur_service = UtilisateurService(self.utilisateurDao)
        self.pseudo = "test_user"
        self.id = "id_user"
        self.mail = "test@example.com"
        self.ddn = "2000-01-01"
        self.mdp = "secure_password"
        self.administrateur = False
        self.organisateur = False
        self.mock_user = [{"pseudo": self.pseudo, "password": self.mdp}]

    def test_creer_compte(self):
        """Test de la création d'un compte utilisateur"""
        # WHEN
        utilisateur = self.utilisateur_service.creer_compte(
            self.pseudo,
            self.id,
            self.mail,
            self.ddn,
            self.mdp,
            self.administrateur,
            self.organisateur,
        )

        # THEN
        self.utilisateurDao.insert_utilisateur.assert_called_once_with(
            id_utilisateur=self.id,
            pseudo=self.pseudo,
            email=self.mail,
            password=self.mdp,
            id_joueur=None,
            administrateur=self.administrateur,
            organisateur=self.organisateur,
            date_de_naissance=self.ddn,
        )

        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.pseudo, self.pseudo)
        self.assertEqual(utilisateur.mail, self.mail)
        self.assertEqual(utilisateur.date_de_naissance, self.ddn)
        self.assertEqual(utilisateur.mdp, self.mdp)
        self.assertEqual(utilisateur.administrateur, self.administrateur)
        self.assertEqual(utilisateur.organisateur, self.organisateur)

    def test_creer_compte_echec_insertion(self):
        """Test d'un échec d'insertion lors de la création de compte"""
        # GIVEN
        self.utilisateurDao.insert_utilisateur.side_effect = Exception("Insertion failed")

        # WHEN / THEN
        with self.assertRaises(Exception):
            self.utilisateur_service.creer_compte(
                self.pseudo, self.mail, self.ddn, self.mdp, self.administrateur, self.organisateur
            )

    def test_se_connecter_utilisateur_succes(self):
        """Test de la connexion réussie d'un utilisateur"""
        # GIVEN
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = self.mock_user

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur(self.pseudo, self.mdp)

        # THEN
        self.utilisateurDao.get_utilisateur_by_parameters.assert_called_with(pseudo=self.pseudo)
        self.assertTrue(result)

    def test_se_connecter_utilisateur_echec(self):
        """Test de la connexion échouée d'un utilisateur (mauvais mot de passe)"""
        # GIVEN
        wrong_mdp = "wrongPassword"
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = [
            {"pseudo": self.pseudo, "password": "password123"}
        ]

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur(self.pseudo, wrong_mdp)

        # THEN
        self.assertFalse(result)

    def test_se_connecter_utilisateur_non_existant(self):
        """Test de la connexion échouée avec un utilisateur non existant"""
        # GIVEN
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = []

        # WHEN
        result = self.utilisateur_service.se_connecter_utilisateur("nonExistantUser", self.mdp)

        # THEN
        self.assertFalse(result)

    def test_pseudo_exist(self):
        """Test de vérification de l'existence d'un pseudo"""
        # GIVEN
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = {"pseudo": "existing_user"}

        # WHEN
        result = self.utilisateur_service.pseudo_exist("existing_user")

        # THEN
        self.assertTrue(result)

    def test_pseudo_n_existe_pas(self):
        """Test de vérification de l'absence d'un pseudo"""
        # GIVEN
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = []

        # WHEN
        result = self.utilisateur_service.pseudo_exist("new_user")

        # THEN
        self.assertFalse(result)

    def test_gestion_exception(self):
        """Test de la gestion des exceptions"""
        # GIVEN
        self.utilisateurDao.get_utilisateur_by_parameters.side_effect = Exception("DB error")

        # WHEN / THEN
        with self.assertRaises(Exception):
            self.utilisateur_service.pseudo_exist("any_user")


if __name__ == "__main__":
    unittest.main()
