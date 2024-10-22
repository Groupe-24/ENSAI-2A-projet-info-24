import unittest
from unittest.mock import MagicMock
from business_object.match import Match
from match_service import MatchService


class TestMatchService(unittest.TestCase):
    def setUp(self):
        self.match_dao_mock = MagicMock()
        self.match_service = MatchService(self.match_dao_mock)

    def test_creer_match(self):
        id_match = 1
        date = "2024-10-22"
        id_tournoi = 101
        equipe_orange = "Team A"
        equipe_bleu = "Team B"

        self.match_dao_mock.insert_match.return_value = None
        match = self.match_service.creer_match(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

        self.assertEqual(match.id_match, id_match)
        self.assertEqual(match.date, date)
        self.assertEqual(match.id_tournoi, id_tournoi)
        self.assertEqual(match.equipe_orange, equipe_orange)
        self.assertEqual(match.equipe_bleu, equipe_bleu)

        self.match_dao_mock.insert_match.assert_called_with(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

    def test_rechercher_match_par_date(self):
        date = "2024-10-22"
        matches = [
            (1, date, 101, "Team A", "Team B"),
            (2, date, 102, "Team C", "Team D"),
        ]

        self.match_dao_mock.get_match_by_date.return_value = matches
        result = self.match_service.rechercher_match_par_date(date)

        self.assertEqual(result, matches)
        self.match_dao_mock.get_match_by_date.assert_called_with(date)

    def test_rechercher_match_par_date_no_matches(self):
        date = "2024-10-22"
        self.match_dao_mock.get_match_by_date.return_value = []  # Aucun match trouvé
        result = self.match_service.rechercher_match_par_date(date)

        self.assertEqual(result, "Il n'existe pas de matches à cette date-là.")

    def test_afficher_calendrier(self):
        matches = [
            (1, "2024-10-22", 101, "Team A", "Team B"),
            (2, "2024-10-23", 102, "Team C", "Team D"),
        ]

        self.match_dao_mock.list_matches.return_value = matches

        # On ne peut pas tester directement les prints, donc on va rediriger stdout
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output  # Rediriger stdout

        self.match_service.afficher_calendrier()

        sys.stdout = sys.__stdout__  # Rétablir stdout

        # Vérifier que le calendrier a été affiché correctement
        expected_output = (
            "Date : 2024-10-22\n"
            "  Match 1 : Team A vs Team B (Tournoi: 101)\n\n"
            "Date : 2024-10-23\n"
            "  Match 2 : Team C vs Team D (Tournoi: 102)\n\n"
        )

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_modifier_match(self):
        id_match = 1
        date = "2024-10-22"
        id_tournoi = 101
        equipe_orange = "Team A"
        equipe_bleu = "Team B"

        self.match_dao_mock.is_in_match.return_value = True  # Simuler l'existence du match
        self.match_dao_mock.update_match.return_value = None  # Pas de retour pour la mise à jour
        self.match_dao_mock.get_match_by_id.return_value = (
            id_match,
            date,
            id_tournoi,
            equipe_orange,
            equipe_bleu,
        )

        result = self.match_service.modifier_match(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

        self.assertEqual(result, (id_match, date, id_tournoi, equipe_orange, equipe_bleu))
        self.match_dao_mock.update_match.assert_called_with(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

    def test_modifier_match_not_found(self):
        id_match = 999  # Match non existant
        self.match_dao_mock.is_in_match.return_value = False  # Simuler que le match n'existe pas

        result = self.match_service.modifier_match(id_match)

        self.assertEqual(result, "Le match n'existe pas.")


if __name__ == "__main__":
    unittest.main()
