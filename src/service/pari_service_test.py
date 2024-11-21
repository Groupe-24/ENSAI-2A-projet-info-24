import unittest
from unittest.mock import MagicMock
from service.pari_service import PariService
from io import StringIO
import sys


class TestPariService(unittest.TestCase):
    def setUp(self):
        self.pari_dao = MagicMock()
        self.pari_service = PariService(self.pari_dao)

        self.match_mock = MagicMock()
        self.match_mock.id_match = "1"
        self.match_mock.equipe_bleu.id_equipe = "bleu_id"
        self.match_mock.equipe_orange.id_equipe = "orange_id"

        self.equipe_mock = MagicMock()
        self.equipe_mock.id_equipe = "bleu_id"

        self.utilisateur_mock = MagicMock()
        self.utilisateur_mock.id_utilisateur = "user1"

    def test_parier(self):
        """Test de la création d'un pari"""
        # GIVEN
        mise = 100
        gain = 200

        self.pari_dao.insert_pari.return_value = None

        # WHEN
        pari = self.pari_service.parier(
            self.match_mock, self.equipe_mock, self.utilisateur_mock, mise, gain
        )

        # THEN
        self.pari_dao.insert_pari.assert_called_once_with(
            id_pari=pari.id_pari,
            id_match=self.match_mock.id_match,
            id_equipe=self.equipe_mock.id_equipe,
            id_utilisateur=self.utilisateur_mock.id_utilisateur,
            mise=mise,
            gain=gain,
        )
        self.assertEqual(pari.mise, mise)
        self.assertEqual(pari.gain, gain)

    def test_afficher_cote(self):
        """Test de l'affichage de la cote d'un match"""
        # GIVEN
        self.pari_dao.list_pari_match.return_value = [
            {"id_equipe": "bleu_id", "mise": 50},
            {"id_equipe": "orange_id", "mise": 50},
        ]

        # WHEN
        cotes = self.pari_service.afficher_cote(self.match_mock)

        # THEN
        self.assertEqual(cotes["cote_equipe_bleu"], 2)
        self.assertEqual(cotes["cote_equipe_orange"], 2)

    def test_gain_potentiel(self):
        """Test du calcul du gain potentiel"""
        # GIVEN
        self.pari_service.afficher_cote = MagicMock(
            return_value={
                "cote_equipe_bleu": 0.5,
                "cote_equipe_orange": 0.5,
                "bleu": "bleu",
                "orange": "orange",
                "match": "1",
            }
        )
        mise = 100

        # WHEN
        gain = self.pari_service.gain_potentiel(mise, self.equipe_mock, self.match_mock)

        # THEN
        self.assertEqual(gain, 150)  # (0.5 + 1) * 100 = 150

    def test_supprimer_pari_existant(self):
        """Test de la suppression d'un pari existant"""
        # GIVEN
        pari_mock = MagicMock()
        pari_mock.id_pari = "123"
        self.pari_dao.exists_by_id.return_value = True  # Le pari existe

        # Capture de la sortie standard pour le test de suppression
        captured_output = StringIO()
        sys.stdout = captured_output

        # WHEN
        self.pari_service.supprimer_pari(pari_mock)

        # THEN
        self.pari_dao.exists_by_id.assert_called_once_with("123")
        self.pari_dao.delete_pari.assert_called_once_with("123")
        self.assertEqual(captured_output.getvalue(), "Le pari a bien été supprimé.\n")

    def test_supprimer_pari_inexistant(self):
        """Test de la suppression d'un pari inexistant"""
        # GIVEN
        pari_mock = MagicMock()
        pari_mock.id_pari = "123"
        self.pari_dao.exists_by_id.return_value = False  # Le pari n'existe pas

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
