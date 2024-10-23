import unittest
from unittest.mock import Mock
from service.match_service import MatchService
import io


class TestMatchService(unittest.TestCase):
    def setUp(self):
        # Given
        self.matchDao = Mock()
        self.match_service = MatchService(self.matchDao)

    def test_rechercher_match_par_date(self):
        # Given: Une date et des matches existants
        date = "2024-10-25"
        self.matchDao.get_match_by_date.return_value = [
            {"id_match": 1, "equipe_orange": "Team A", "equipe_bleu": "Team B"}
        ]

        # When: On recherche les matches par date
        result = self.match_service.rechercher_match_par_date(date)

        # Then: Le résultat doit être les matches trouvés
        self.assertEqual(
            result, [{"id_match": 1, "equipe_orange": "Team A", "equipe_bleu": "Team B"}]
        )

    def test_rechercher_match_par_date_aucun_match(self):
        # Given: Une date sans matches
        date = "2024-10-25"
        self.matchDao.get_match_by_date.return_value = []

        # When: On recherche les matches par date
        result = self.match_service.rechercher_match_par_date(date)

        # Then: On doit recevoir un message indiquant qu'aucun match n'existe
        self.assertEqual(result, "Il n'existe pas de matches à cette date-là.")

    def test_afficher_calendrier_aucun_match(self):
        # Given: Aucun match prévu
        self.matchDao.list_matches.return_value = []

        # When: On affiche le calendrier
        result = self.match_service.afficher_calendrier()

        # Then: Le résultat doit indiquer qu'il n'y a aucun match
        self.assertEqual(result, "Aucun match prévu.")

    def test_afficher_calendrier_avec_match(self):
        # Given: Des matches prévus
        matches = [
            (1, "2024-10-25", 101, "Team A", "Team B"),
            (2, "2024-10-26", 102, "Team C", "Team D"),
        ]
        self.matchDao.list_matches.return_value = matches

        expected_output = (
            "Date : 2024-10-25\n"
            "  Match 1 : Team A vs Team B (Tournoi: 101)\n\n"
            "Date : 2024-10-26\n"
            "  Match 2 : Team C vs Team D (Tournoi: 102)\n\n"
        )

        # When: On affiche le calendrier
        with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.match_service.afficher_calendrier()
            output = mock_stdout.getvalue()

        # Then: Le résultat doit correspondre à la sortie attendue
        self.assertEqual(output, expected_output)

    def test_creer_match(self):
        # Given: Des détails de match pour la création
        id_match = 1
        date = "2024-10-25"
        id_tournoi = 101
        equipe_orange = "Team A"
        equipe_bleu = "Team B"

        # When: On crée un match
        match = self.match_service.creer_match(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )

        # Then: On doit appeler insert_match avec les bons arguments
        self.matchDao.insert_match.assert_called_once_with(
            id_match, date, id_tournoi, equipe_orange, equipe_bleu
        )
        self.assertIsNotNone(match)  # Vérifier que l'objet match a été créé

    def test_modifier_match_inexistant(self):
        # Given: Un ID de match inexistant
        id_match = 1
        self.matchDao.is_in_match.return_value = False

        # When: On essaie de modifier ce match
        result = self.match_service.modifier_match(id_match)

        # Then: On doit recevoir un message indiquant que le match n'existe pas
        self.assertEqual(result, "Le match n'existe pas.")

    def test_modifier_match_existant(self):
        # Given: Un match existant
        id_match = 1
        self.matchDao.is_in_match.return_value = True
        self.matchDao.get_match_by_id.return_value = {
            "id": 1,
            "date": "2024-10-26",
            "id_tournoi": 101,
            "equipe_orange": "Team A",
            "equipe_bleu": "Team B",
        }

        # When: On modifie ce match
        result = self.match_service.modifier_match(
            id_match,
            date="2024-10-26",
            id_tournoi=101,
            equipe_orange="Team A",
            equipe_bleu="Team B",
        )

        # Then: On doit appeler update_match avec les bons arguments
        self.matchDao.update_match.assert_called_once_with(
            id_match,
            date="2024-10-26",
            id_tournoi=101,
            equipe_orange="Team A",
            equipe_bleu="Team B",
        )
        self.assertEqual(result["date"], "2024-10-26")


if __name__ == "__main__":
    unittest.main()
