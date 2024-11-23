import unittest
from unittest.mock import MagicMock
from statistique_service import StatistiqueService


class TestStatistiqueService(unittest.TestCase):
    def setUp(self):
        self.mock_dao = MagicMock()
        self.service = StatistiqueService(self.mock_dao)

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

    def obtenir_statistiques_joueur(self, joueur):
        result = self.dao.statistique_joueur(joueur)
        if not result:
            raise ValueError(f"Aucune statistique trouvée pour le joueur {joueur}.")
        return {"joueur": result[0], "total_buts": result[1], "total_scores": result[2]}


if __name__ == "__main__":
    unittest.main()
