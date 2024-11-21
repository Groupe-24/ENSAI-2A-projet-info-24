import unittest
from unittest.mock import MagicMock
from business_object.users.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService


class TestUtilisateurService(unittest.TestCase):
    def setUp(self):
        self.utilisateurDao = MagicMock()
        self.utilisateur_service = UtilisateurService(self.utilisateurDao)

        # GIVEN
        self.pseudo = "test_user"
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
            self.pseudo, self.mail, self.ddn, self.mdp, self.administrateur, self.organisateur
        )

        # THEN
        self.utilisateurDao.insert_utilisateur.assert_called_once_with(
            self.pseudo, self.mail, self.ddn, self.mdp, self.administrateur, self.organisateur
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

        # THEN: Vérifications
        self.utilisateurDao.get_utilisateur_by_parameters.assert_called_with(pseudo=self.pseudo)
        self.assertTrue(result)

    def test_se_connecter_utilisateur_echec(self):
        """Test de la connexion échouée d'un utilisateur (mauvais mot de passe)"""
        # GIVEN: Simuler un utilisateur avec un mauvais mot de passe
        wrong_mdp = "wrongPassword"
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = [
            {"pseudo": self.pseudo, "password": "password123"}
        ]

        # WHEN: Connexion avec un mot de passe incorrect
        result = self.utilisateur_service.se_connecter_utilisateur(self.pseudo, wrong_mdp)

        # THEN: Vérification de l'échec de la connexion
        self.assertFalse(result)

    def test_se_connecter_utilisateur_non_existant(self):
        """Test de la connexion échouée avec un utilisateur non existant"""
        # GIVEN: Aucun utilisateur trouvé pour le pseudo donné
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = []

        # WHEN: Connexion avec un pseudo inexistant
        result = self.utilisateur_service.se_connecter_utilisateur("nonExistantUser", self.mdp)

        # THEN: Vérification de l'échec
        self.assertFalse(result)

    def test_pseudo_exist(self):
        """Test de vérification de l'existence d'un pseudo"""
        # GIVEN: Un utilisateur avec le pseudo "existing_user"
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = {"pseudo": "existing_user"}

        # WHEN: Vérification de l'existence du pseudo
        result = self.utilisateur_service.pseudo_exist("existing_user")

        # THEN: Vérification que le pseudo existe
        self.assertTrue(result)

    def test_pseudo_n_existe_pas(self):
        """Test de vérification de l'absence d'un pseudo"""
        # GIVEN: Aucun utilisateur trouvé pour le pseudo "new_user"
        self.utilisateurDao.get_utilisateur_by_parameters.return_value = None

        # WHEN: Vérification de l'existence du pseudo
        result = self.utilisateur_service.pseudo_exist("new_user")

        # THEN: Vérification que le pseudo n'existe pas
        self.assertFalse(result)

    def test_gestion_exception(self):
        """Test de la gestion des exceptions"""
        # GIVEN: Une erreur de base de données
        self.utilisateurDao.get_utilisateur_by_parameters.side_effect = Exception("DB error")

        # WHEN / THEN: Vérification que l'exception est levée
        with self.assertRaises(Exception):
            self.utilisateur_service.pseudo_exist("any_user")


if __name__ == "__main__":
    unittest.main()
