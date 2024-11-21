import unittest
from unittest.mock import MagicMock
from service.joueur_service import JoueurService


class TestJoueurService(unittest.TestCase):
    def setUp(self):
        self.joueur_dao = MagicMock()
        self.joueur_service = JoueurService(self.joueur_dao)

    def test_rechercher_joueur_trouve(self):
        """Test de la recherche d'un joueur avec un pseudo existant"""
        # GIVEN
        pseudo = "jp"
        self.joueur_dao.get_joueur_by_parameters.return_value = [
            {"id_joueurs": 1, "pseudo": "jp", "equipe": "Equipe1", "professionnel": True}
        ]

        # WHEN
        result = self.joueur_service.rechercher_joueur(pseudo)

        # THEN
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].pseudo, "jp")
        self.assertEqual(result[0].equipe, "Equipe1")
        self.assertTrue(result[0].professionnel)

    def test_rechercher_joueur_non_trouve(self):
        """Test de la recherche d'un joueur avec un pseudo inexistant"""
        # GIVEN
        pseudo = "inexistant"
        self.joueur_dao.get_joueur_by_parameters.return_value = []

        # WHEN
        result = self.joueur_service.rechercher_joueur(pseudo)

        # THEN
        self.assertFalse(result)

    def test_creer_joueur_succes(self):
        """Test de la création d'un joueur avec succès"""
        # GIVEN
        self.joueur_dao.exists_by_id.return_value = False
        self.joueur_dao.get_joueur_by_parameters.return_value = None

        # WHEN
        result = self.joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

        # THEN
        self.assertEqual(result, "Le joueur 'PseudoTest' a été créé avec succès.")
        self.joueur_dao.insert_joueur.assert_called_once_with(
            id_joueur=1, pseudo="PseudoTest", equipe="EquipeTest", professionnel=True
        )

    def test_creer_joueur_pseudo_existant(self):
        """Test pour vérifier qu'un joueur avec un pseudo existant ne peut pas être créé"""
        # GIVEN
        self.joueur_dao.exists_by_id.return_value = False
        self.joueur_dao.get_joueur_by_parameters.return_value = [{"pseudo": "PseudoTest"}]

        # WHEN
        result = self.joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

        # THEN
        self.assertEqual(result, "Un joueur avec le pseudo 'PseudoTest' existe déjà.")
        self.joueur_dao.insert_joueur.assert_not_called()

    def test_creer_joueur_id_existant(self):
        """Test pour vérifier qu'un joueur avec un ID existant ne peut pas être créé"""
        # GIVEN
        self.joueur_dao.exists_by_id.return_value = True

        # WHEN
        result = self.joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

        # THEN
        self.assertEqual(result, "Un joueur avec l'ID 1 existe déjà.")
        self.joueur_dao.insert_joueur.assert_not_called()

    def test_supprimer_joueur_succes(self):
        """Test de la suppression réussie d'un joueur existant"""
        # GIVEN
        self.joueur_dao.exists_by_id.return_value = True

        # WHEN
        result = self.joueur_service.supprimer_joueur(1)

        # THEN
        self.assertEqual(result, "Le joueur avec l'ID 1 a été supprimé avec succès.")
        self.joueur_dao.delete_joueur.assert_called_once_with(1)

    def test_supprimer_joueur_inexistant(self):
        """Test de la suppression d'un joueur inexistant"""
        # GIVEN
        self.joueur_dao.exists_by_id.return_value = False

        # WHEN
        result = self.joueur_service.supprimer_joueur(1)

        # THEN
        self.assertEqual(result, "Le joueur avec l'ID 1 n'existe pas.")
        self.joueur_dao.delete_joueur.assert_not_called()


if __name__ == "__main__":
    unittest.main()
