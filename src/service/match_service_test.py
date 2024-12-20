import unittest
from unittest.mock import MagicMock
from service.match_service import MatchService
import io


class TestMatchService(unittest.TestCase):
    def setUp(self):
        self.matchDao = MagicMock()
        self.match_service = MatchService(self.matchDao)

    def test_rechercher_match_par_date(self):
        """Test de la recherche d'un match existant selon une date"""
        # Given
        date = "2024-10-25"
        self.matchDao.get_match_by_date.return_value = [
            {"id_match": 1, "equipe_orange": "Team A", "equipe_bleu": "Team B"}
        ]

        # When
        result = self.match_service.rechercher_match_par_date(date)

        # Then
        self.assertEqual(
            result, [{"id_match": 1, "equipe_orange": "Team A", "equipe_bleu": "Team B"}]
        )

    def test_rechercher_match_par_date_aucun_match(self):
        """Test de la recherche d'un match inexistant selon une date"""
        # Given
        date = "2024-10-25"
        self.matchDao.get_match_by_date.return_value = []

        # When
        result = self.match_service.rechercher_match_par_date(date)

        # Then
        self.assertEqual(result, "Il n'existe pas de matches à cette date-là.")

    def test_afficher_calendrier_aucun_match(self):
        """Test de l'affichage du calendrier des matchs vide"""
        # Given
        self.matchDao.list_matches.return_value = []

        # When
        result = self.match_service.afficher_calendrier()

        # Then
        self.assertEqual(result, "Aucun match prévu.")

    def test_afficher_calendrier_avec_match(self):
        """Test de l'affichage du calendrier des matchs avec des valeurs"""

        # GIVEN
        matches = [
            {
                "id_matches": 1,
                "date": "2024-10-25",
                "id_tournois": 101,
                "equipe_orange": "Team A",
                "equipe_bleu": "Team B",
            },
            {
                "id_matches": 2,
                "date": "2024-10-26",
                "id_tournois": 102,
                "equipe_orange": "Team C",
                "equipe_bleu": "Team D",
            },
        ]
        self.matchDao.list_matches.return_value = matches

        self.equipeDao_mock = MagicMock()
        self.equipeDao_mock.get_equipe_by_id = MagicMock(
            side_effect=lambda equipe_id: {"nom": equipe_id}
        )
        self.tournoiDao_mock = MagicMock()
        self.tournoiDao_mock.get_tournoi_by_id = MagicMock(
            side_effect=lambda tournoi_id: {"titre": f"Tournoi {tournoi_id}"}
        )
        expected_output = (
            "Date : 2024-10-25\n"
            "  Match 1 : Team A vs Team B (Tournoi: Tournoi 101)\n\n"
            "Date : 2024-10-26\n"
            "  Match 2 : Team C vs Team D (Tournoi: Tournoi 102)\n\n"
        )

        # WHEN
        with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with unittest.mock.patch("service.match_service.EquipeDAO") as mock_EquipeDAO:
                mock_EquipeDAO.return_value = self.equipeDao_mock
                with unittest.mock.patch("service.match_service.TournoiDAO") as mock_TournoiDAO:
                    mock_TournoiDAO.return_value = self.tournoiDao_mock
                    self.match_service.afficher_calendrier()

            output = mock_stdout.getvalue()

        # THEN
        self.assertEqual(output.strip(), expected_output.strip())

    def test_creer_match(self):
        """Test de la création d'un match"""
        # Given
        id_match = 1
        date = "2024-10-25"
        id_tournoi = 101
        equipe_orange = "Team A"
        equipe_bleu = "Team B"

        # When
        match = self.match_service.creer_match(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

        # Then
        self.matchDao.insert_match.assert_called_once_with(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )
        self.assertIsNotNone(match)

    def test_modifier_match_inexistant(self):
        """test de la modification d'un match inexistant"""
        # Given
        id_match = 1
        self.matchDao.is_in_match.return_value = False

        # When
        result = self.match_service.modifier_match(id_match)

        # Then
        self.assertEqual(result, "Le match n'existe pas.")

    def test_modifier_match_existant(self):
        """Test de la modification d'un match existant"""
        # Given
        id_match = 1
        self.matchDao.is_in_match.return_value = True
        self.matchDao.get_match_by_id.return_value = {
            "id": 1,
            "date": "2024-10-26",
            "id_tournoi": 101,
            "equipe_orange": "Team A",
            "equipe_bleu": "Team B",
        }

        # When
        result = self.match_service.modifier_match(
            id_match,
            "2024-10-26",
            101,
            "Team A",
            "Team B",
        )

        # Then
        self.matchDao.update_match.assert_called_once_with(
            id_match,
            "2024-10-26",
            101,
            "Team A",
            "Team B",
        )
        self.assertEqual(result["date"], "2024-10-26")

    def test_supprimer_match_existant(self):
        """Test de la suppresion d'un match existant"""
        # Given
        id_match = 1
        self.matchDao.is_in_match.return_value = True
        self.matchDao.delete_match.return_value = None

        # When
        result = self.match_service.supprimer_match(id_match)

        # Then
        self.assertEqual(result, f"Match avec l'ID {id_match} supprimé avec succès.")
        self.matchDao.delete_match.assert_called_once_with(id_match)

    def test_supprimer_match_inexistant(self):
        """Test de la suppression d'un match inexistant"""
        # Given
        id_match = 1
        self.matchDao.is_in_match.return_value = False
        # When
        result = self.match_service.supprimer_match(id_match)

        # Then
        self.assertEqual(result, "Le match n'existe pas.")
        self.matchDao.delete_match.assert_not_called()


if __name__ == "__main__":
    unittest.main()
