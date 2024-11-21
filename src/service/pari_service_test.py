import unittest
from unittest.mock import MagicMock
from service.pari_service import PariService
from io import StringIO
import sys


class TestPariService(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.pari_dao = MagicMock()
        self.pari_service = PariService(self.pari_dao)

    def test_parier(self):
        """Test de la création d'un pari"""

        # GIVEN
        pari_dao_mock = MagicMock()
        pari_dao_mock.insert_pari = MagicMock()

        # Création des mocks pour match, équipe et utilisateur
        match_mock = MagicMock()
        match_mock.id_match = "1"

        equipe_mock = MagicMock()
        equipe_mock.id_equipe = "10"

        utilisateur_mock = MagicMock()
        utilisateur_mock.id_utilisateur = "100"

        # Création du service avec le mock
        pari_service = PariService(pari_dao_mock)

        # WHEN
        pari = pari_service.parier(
            match=match_mock, equipe=equipe_mock, utilisateur=utilisateur_mock, mise=150, gain=None
        )

        # THEN
        self.assertIsNotNone(pari.id_pari)
        self.assertEqual(pari.mise, 150)
        pari_dao_mock.insert_pari.assert_called_once_with(
            id_pari=pari.id_pari,
            id_match="1",
            id_equipe="10",
            id_utilisateur="100",
            mise=150,
            gain=None,
        )

    def test_afficher_cote(self):
        """Test de la méthode afficher_cote"""

        # GIVEN
        equipe_bleu_mock = MagicMock()
        equipe_bleu_mock.id_equipe = "1"

        equipe_orange_mock = MagicMock()
        equipe_orange_mock.id_equipe = "2"

        match_mock = MagicMock()
        match_mock.id_match = "101"
        match_mock.equipe_bleu = equipe_bleu_mock
        match_mock.equipe_orange = equipe_orange_mock

        resultat_paris = [
            {"id_equipe": "1", "mise": 100},  # pari équipe bleue
            {"id_equipe": "2", "mise": 150},  # pari équipe orange
            {"id_equipe": "1", "mise": 50},
        ]

        # Simulation du retour de la méthode `list_pari_match`
        self.pari_dao.list_pari_match.return_value = resultat_paris

        # WHEN
        result = self.pari_service.afficher_cote(match_mock)

        # THEN
        cote_equipe_bleu = (100 + 50) / (100 + 50 + 150)
        cote_equipe_orange = 150 / (100 + 50 + 150)

        self.assertEqual(result["match"], "101")
        self.assertEqual(result["1"], "bleu")
        self.assertEqual(result["2"], "orange")
        self.assertEqual(result["cote_equipe_bleu"], cote_equipe_bleu)
        self.assertEqual(result["cote_equipe_orange"], cote_equipe_orange)

        self.pari_dao.list_pari_match.assert_called_once_with("101")

        # Capture de la sortie standard
        captured_output = StringIO()
        sys.stdout = captured_output

        expected_output = (
            f"Cote equipe bleu : {cote_equipe_bleu}\n"
            f"Cote equipe orange : {cote_equipe_orange}\n"
        )

        # WHEN (vérification de la sortie)
        self.pari_service.afficher_cote(match_mock)

        # THEN
        self.assertEqual(captured_output.getvalue(), expected_output)

        # Restauration de la sortie standard
        sys.stdout = sys.__stdout__

    def test_gain_potentiel(self):
        """Test de la méthode gain_potentiel"""

        # Test 1: Erreur d'une équipe qui ne fait pas partie du match
        # GIVEN
        equipe_mock = MagicMock()
        equipe_mock.id_equipe = "3"

        equipe_bleu_mock = MagicMock()
        equipe_bleu_mock.id_equipe = "1"

        equipe_orange_mock = MagicMock()
        equipe_orange_mock.id_equipe = "2"

        match_mock = MagicMock()
        match_mock.id_match = "101"
        match_mock.equipe_bleu = equipe_bleu_mock
        match_mock.equipe_orange = equipe_orange_mock

        # WHEN / THEN:
        with self.assertRaises(ValueError, msg="L'équipe doit jouer dans le match spécifié."):
            self.pari_service.gain_potentiel(100, equipe_mock, match_mock)

        # Test 2 : Cas classique
        # GIVEN
        cotes_mock = {
            "match": "101",
            "1": "bleu",
            "2": "orange",
            "cote_equipe_bleu": 1.5,
            "cote_equipe_orange": 2.0,
        }
        self.pari_service.afficher_cote = MagicMock(return_value=cotes_mock)

        # WHEN:
        mise = 100
        gain_potentiel = self.pari_service.gain_potentiel(mise, equipe_bleu_mock, match_mock)

        # THEN:
        expected_gain = (1.5 + 1) * mise  # 2.5 * 100 = 250
        self.assertEqual(gain_potentiel, expected_gain)
        self.pari_service.afficher_cote.assert_called_once_with(match_mock)


def test_supprimer_pari(self):
    """Test de la méthode supprimer_pari pour un pari existant et inexistant"""

    # Test 1 : Pari Existant
    # GIVEN
    pari_mock = MagicMock()
    pari_mock.id_pari = "123"
    self.pari_dao.exists_by_id.return_value = True

    # Capture de la sortie standard pour le premier cas
    captured_output = StringIO()
    sys.stdout = captured_output

    # WHEN
    self.pari_service.supprimer_pari(pari_mock)

    # THEN
    self.pari_dao.exists_by_id.assert_called_once_with("123")
    self.pari_dao.delete_pari.assert_called_once_with("123")
    self.assertEqual(captured_output.getvalue(), "Le pari a bien été supprimé.\n")

    # Test 2 : Pari inexistant
    # GIVEN
    self.pari_dao.reset_mock()
    self.pari_dao.exists_by_id.return_value = False

    # WHEN / THEN: Vérification que l'exception est bien levée
    with self.assertRaises(ValueError) as context:
        self.pari_service.supprimer_pari(pari_mock)

    # THEN: Vérification du message d'erreur
    self.assertEqual(str(context.exception), "Le pari n'existe pas.")
    self.pari_dao.exists_by_id.assert_called_once_with("123")
    self.pari_dao.delete_pari.assert_not_called()

    # Restauration de la sortie standard
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
