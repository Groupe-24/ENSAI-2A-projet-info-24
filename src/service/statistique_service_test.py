import unittest
from unittest.mock import MagicMock
from statistique_service import StatistiqueService


class TestStatistiqueService(unittest.TestCase):
    def setUp(self):
        self.mock_dao = MagicMock()
        self.service = StatistiqueService(self.mock_dao)

    def test_ajouter_statistique(self):
        self.mock_dao.exists_by_id.return_value = False
        result = self.service.ajouter_statistique(1, "Joueur1", "Match1", "EquipeA", 3, 1500, 200)
        self.mock_dao.insert_statistique.assert_called_once_with(
            1, "Joueur1", "Match1", "EquipeA", 3, 1500, 200
        )
        self.assertEqual(result, "Statistique ajoutée avec succès pour l'ID 1.")

    def test_ajouter_statistique_existante(self):
        self.mock_dao.exists_by_id.return_value = True
        with self.assertRaises(ValueError) as context:
            self.service.ajouter_statistique(1, "Joueur1", "Match1", "EquipeA", 3, 1500, 200)
        self.assertEqual(str(context.exception), "La statistique avec l'ID 1 existe déjà.")

    def test_obtenir_statistique(self):
        self.mock_dao.get_statistique_by_id.return_value = (
            1,
            "Joueur1",
            "Match1",
            "EquipeA",
            3,
            1500,
            200,
        )
        result = self.service.obtenir_statistique(1)
        self.mock_dao.get_statistique_by_id.assert_called_once_with(1)
        self.assertEqual(result, (1, "Joueur1", "Match1", "EquipeA", 3, 1500, 200))

    def test_obtenir_statistique_inexistante(self):
        self.mock_dao.get_statistique_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.service.obtenir_statistique(99)
        self.assertEqual(str(context.exception), "Aucune statistique trouvée avec l'ID 99.")

    def test_mettre_a_jour_statistique(self):
        self.mock_dao.exists_by_id.return_value = True
        result = self.service.mettre_a_jour_statistique(1, but=5, score_de_match=1600)
        self.mock_dao.update_statistique.assert_called_once_with(1, but=5, score_de_match=1600)
        self.assertEqual(result, "Statistique avec l'ID 1 mise à jour avec succès.")

    def test_supprimer_statistique(self):

        self.mock_dao.exists_by_id.return_value = True
        result = self.service.supprimer_statistique(1)
        self.mock_dao.delete_statistique.assert_called_once_with(1)
        self.assertEqual(result, "Statistique avec l'ID 1 supprimée avec succès.")

    def test_obtenir_statistiques_equipe(self):
        self.mock_dao.statistique_equipe.return_value = ("EquipeA", 5, 2900)
        result = self.service.obtenir_statistiques_equipe("EquipeA")
        self.mock_dao.statistique_equipe.assert_called_once_with("EquipeA")
        self.assertEqual(result, {"equipe": "EquipeA", "total_buts": 5, "total_scores": 2900})

    def test_obtenir_statistiques_match(self):
        self.mock_dao.statistique_match.return_value = [
            ("Match1", 3, 1500),
            ("Match2", 4, 1700),
        ]
        result = self.service.obtenir_statistiques_match("Match1")
        self.mock_dao.statistique_match.assert_called_once_with("Match1")
        self.assertEqual(result, [{"match": "Match1", "total_buts": 3, "total_scores": 1500}])

    def test_obtenir_statistique_joueur(self):
        self.mock_dao.statistique_joueur.return_value = [("joueur1", 1, 300)]
        result = self.service.obtenir_statistiques_joueur("joueur1")
        self.mock_dao.statistique_joueurassert_called_once_with("joueur1")
        self.assertEqual(result, [{"joueur": "joueur1", "total_buts": 1, "total_scores": 300}])

    print("OK")
