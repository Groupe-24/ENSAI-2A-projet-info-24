from unittest.mock import MagicMock
from service.tournoi_service import TournoiService
from dao.tournoi_dao import TournoiDAO
from business_object.tournoi import Tournoi
import unittest


class TestTournoiService(unittest.TestCase):
    def setUp(self):
        self.tournoi_dao_mock = MagicMock(TournoiDAO)
        self.organisateur_mock = MagicMock()
        self.organisateur_mock.id = "organisateur_test"
        self.tournoi_service = TournoiService(self.tournoi_dao_mock)

    def test_creer_tournoi(self):
        """Test de la création d'un tournoi"""
        # GIVEN
        self.tournoi_dao_mock.insert_tournoi = MagicMock()
        # WHEN
        tournoi = self.tournoi_service.creer_tournoi(
            titre="Tournoi Test",
            description="Description du tournoi",
            date_debut="2024-01-01",
            date_fin="2024-01-02",
            organisateur=self.organisateur_mock,
        )
        # THEN
        self.assertIsNotNone(tournoi.id_tournoi)
        self.assertEqual(tournoi.titre, "Tournoi Test")
        self.assertEqual(tournoi.description, "Description du tournoi")
        self.assertEqual(tournoi.date_debut, "2024-01-01")
        self.assertEqual(tournoi.date_fin, "2024-01-02")
        self.assertEqual(tournoi.id_organisateur, "organisateur_test")
        self.tournoi_dao_mock.insert_tournoi.assert_called_once_with(
            id_tournoi=tournoi.id_tournoi,
            titre="Tournoi Test",
            description="Description du tournoi",
            date_debut="2024-01-01",
            date_fin="2024-01-02",
            id_organisateur="organisateur_test",
        )

    def test_lister_tournois(self):
        """Test de la liste des tournois"""
        # GIVEN
        self.tournoi_dao_mock.list_tournois = MagicMock(
            return_value=[
                {
                    "id_tournois": "1",
                    "titre": "Tournoi 1",
                    "description": "Description 1",
                    "date_debut": "2024-01-01",
                    "date_fin": "2024-01-02",
                    "id_organisateur": "organisateur_1",
                    "id_equipe": "equipe_1",
                }
            ]
        )

        # WHEN
        result = self.tournoi_service.lister_tournois()

        # THEN : Vérifications sur les tournois retournés
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id_tournoi, "1")
        self.assertEqual(result[0].titre, "Tournoi 1")
        self.assertEqual(result[0].description, "Description 1")

    def test_rechercher_tournoi_nom(self):
        """Test de la recherche d'un tournoi par nom"""

        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(
            return_value=[
                {
                    "id_tournois": "2",
                    "titre": "Tournoi Recherche",
                    "description": "Description Recherche",
                    "date_debut": "2024-01-03",
                    "date_fin": "2024-01-04",
                    "id_organisateur": "organisateur_2",
                    "id_equipe": "equipe_2",  # Assurez-vous que cette clé existe si vous l'utilisez
                }
            ]
        )

        # WHEN
        result = self.tournoi_service.rechercher_tournoi_nom("Tournoi Recherche")

        # THEN
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].titre, "Tournoi Recherche")
        self.assertEqual(result[0].id_tournoi, "2")

    def test_supprimer_tournoi(self):
        """Test de la suppression d'un tournoi"""

        # Test 1 : tournoi existant
        # GIVEN : Configuration du mock pour un tournoi existant
        self.tournoi_dao_mock.get_tournoi_by_id = MagicMock(
            return_value={"id_tournoi": "1", "titre": "Tournoi 1"}
        )
        self.tournoi_dao_mock.delete_tournoi = MagicMock()

        tournoi = Tournoi(
            id_tournoi="1",
            titre="Tournoi Test",
            description="Description du tournoi",
            date_debut="2024-01-01",
            date_fin="2024-01-02",
            id_organisateur=self.organisateur_mock.id,
        )

        # WHEN : Suppression du tournoi
        resultat = self.tournoi_service.supprimer_tournoi(tournoi.id_tournoi)

        # THEN : Vérifications sur la suppression
        self.assertEqual(resultat, "Le tournoi a bien été supprimé.")
        self.tournoi_dao_mock.delete_tournoi.assert_called_once_with("1")

        # Test 2 : tournoi inexistant
        # GIVEN : Configuration du mock pour un tournoi inexistant
        self.tournoi_dao_mock.reset_mock()
        self.tournoi_dao_mock.get_tournoi_by_id = MagicMock(return_value=None)

        tournoi_inexistant = Tournoi(
            id_tournoi="999",
            titre="Tournoi Inexistant",
            description="Description du tournoi",
            date_debut="2024-01-01",
            date_fin="2024-01-02",
            id_organisateur=self.organisateur_mock.id,
        )

        # WHEN
        with self.assertRaises(ValueError) as context:
            self.tournoi_service.supprimer_tournoi(tournoi_inexistant.id_tournoi)

        # THEN
        self.assertEqual(str(context.exception), "Le tournoi spécifié n'existe pas.")
        self.tournoi_dao_mock.delete_tournoi.assert_not_called()

    def test_equipe_dans_le_tournoi(self):
        """Test de la méthode equipe_dans_le_tournoi"""

        # Test 1 : Cas où le tournoi n'existe pas
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(return_value=[])
        # WHEN
        result = self.tournoi_service.equipe_dans_le_tournoi("Tournoi Inexistant", "Equipe A")
        # THEN
        self.assertFalse(result)

        # Test 2 : Cas où le tournoi existe et l'équipe est inscrite
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(
            return_value=[{"id_equipe": "Equipe A, Equipe B, Equipe C"}]
        )
        # WHEN
        result = self.tournoi_service.equipe_dans_le_tournoi("Tournoi Test", "Equipe A")
        # THEN
        self.assertTrue(result)

        # Test 3 : Cas où le tournoi existe mais l'équipe n'est pas inscrite
        # WHEN
        result = self.tournoi_service.equipe_dans_le_tournoi("Tournoi Test", "Equipe D")
        # THEN
        self.assertFalse(result)

        # Test 4 : Cas où il n'y a pas d'équipe inscrite
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(return_value=[{"id_equipe": None}])
        # WHEN
        result = self.tournoi_service.equipe_dans_le_tournoi("Tournoi Test", "Equipe A")
        # THEN
        self.assertFalse(result)

    def test_ajout_equipe(self):
        """Test de l'ajout d'une équipe à un tournoi"""

        # 1. Cas où l'équipe n'est pas inscrite dans le tournoi et le tournoi n'a pas
        # encore d'équipe
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(
            return_value=[{"id_tournois": "1", "id_equipe": None}]
        )
        self.tournoi_dao_mock.equipe_dans_le_tournoi = MagicMock(return_value=False)

        # WHEN
        self.tournoi_service.ajout_equipe("Tournoi Test", "Equipe A")

        # THEN
        self.tournoi_dao_mock.update_tournoi.assert_called_once_with(
            id_tournoi="1", id_equipe="Equipe A"
        )

        self.tournoi_dao_mock.reset_mock()

        # 2. Cas où le tournoi a déjà une équipe inscrite
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(
            return_value=[{"id_tournois": "1", "id_equipe": "Equipe B"}]
        )
        self.tournoi_dao_mock.equipe_dans_le_tournoi = MagicMock(return_value=False)

        # WHEN
        self.tournoi_service.ajout_equipe("Tournoi Test", "Equipe A")

        # THEN
        self.tournoi_dao_mock.update_tournoi.assert_called_once_with(
            id_tournoi="1", id_equipe="Equipe B, Equipe A"
        )

        self.tournoi_dao_mock.reset_mock()

        # 3. Cas où l'équipe est déjà inscrite
        # GIVEN
        self.tournoi_dao_mock.get_tournoi_by_titre = MagicMock(
            return_value=[{"id_tournoi": "1", "id_equipe": "Equipe A"}]
        )
        self.tournoi_dao_mock.equipe_dans_le_tournoi = MagicMock(return_value=True)

        # WHEN
        self.tournoi_service.ajout_equipe("Tournoi Test", "Equipe A")

        # THEN
        self.tournoi_dao_mock.update_tournoi.assert_not_called()


if __name__ == "__main__":
    unittest.main()
