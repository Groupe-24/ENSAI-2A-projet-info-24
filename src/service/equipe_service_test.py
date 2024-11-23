import unittest
from unittest.mock import MagicMock
from service.equipe_service import EquipeService
from business_object.equipe import Equipe


class TestEquipeService(unittest.TestCase):
    def setUp(self):
        self.equipeDao = MagicMock()
        self.equipe_service = EquipeService(self.equipeDao)

    def test_lister_equipes(self):
        """Test de la liste de toutes les équipes"""
        # Given
        self.equipeDao.list_equipes.return_value = [
            {"id_equipe": 1, "nom": "Equipe 1"},
            {"id_equipe": 2, "nom": "Equipe 2"},
        ]

        # When
        result = self.equipe_service.lister_equipes()

        # Then
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Equipe)
        self.assertEqual(result[0].id_equipe, 1)
        self.assertEqual(result[0].nom, "Equipe 1")

    def test_rechercher_equipe_existe(self):
        """Test de la recherche d'une équipe existante selon l'id"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id_equipe": 1, "nom": "Equipe 1"}

        # When
        result = self.equipe_service.rechercher_equipe(1)

        # Then
        self.assertIsInstance(result, Equipe)
        self.assertEqual(result.id_equipe, 1)
        self.assertEqual(result.nom, "Equipe 1")

    def test_rechercher_equipe_n_existe_pas(self):
        """Test de la recherche d'une équipe inexistante selon l'id"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = None

        # When & Then
        with self.assertRaises(ValueError):
            self.equipe_service.rechercher_equipe(999)

    def test_ajouter_equipe(self):
        """Test d'ajout d'une équipe"""
        # Given
        self.equipeDao.insert_equipe.return_value = True

        # When
        self.equipe_service.ajouter_equipe("Nouvelle Equipe")

        # Then
        self.equipeDao.insert_equipe.assert_called_once_with("Nouvelle Equipe")

    def test_modifier_equipe(self):
        """Test de modification d'une information d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id_equipe": 1, "nom": "Ancienne Equipe"}

        # When
        result = self.equipe_service.modifier_equipe(1, nom_modif="Nouvelle Equipe")

        # Then
        self.assertEqual(result.nom, "Nouvelle Equipe")
        self.equipeDao.update_equipe.assert_called_once_with(
            {"id_equipe": 1, "nom": "Nouvelle Equipe"}
        )

    def test_supprimer_equipe(self):
        """Test de suppression d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id_equipe": 1, "nom": "Equipe à supprimer"}

        # When
        result = self.equipe_service.supprimer_equipe(1)

        # Then
        self.assertEqual(result, "Équipe supprimée avec succès")
        self.equipeDao.delete_equipe.assert_called_once_with(1)

    def test_lister_equipes_par_nom(self):
        """Test de la liste d'équipes selon le nom"""
        # Given
        self.equipeDao.list_equipes_by_name.return_value = [
            {"id_equipe": 1, "nom": "Equipe A"},
            {"id_equipe": 2, "nom": "Equipe B"},
        ]

        # When
        result = self.equipe_service.lister_equipes_par_nom("Equipe")

        # Then
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Equipe)
        self.assertEqual(result[0].nom, "Equipe A")

    def test_lister_equipes_par_tournoi(self):
        """Test de la liste d'équipes selon le tournoi"""
        # Given
        self.equipeDao.list_equipes_by_tournoi.return_value = [
            {"id_equipe": 1, "nom": "Equipe A"},
            {"id_equipe": 2, "nom": "Equipe B"},
        ]

        # When
        result = self.equipe_service.lister_equipes_par_tournoi(1)

        # Then
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Equipe)
        self.assertEqual(result[0].nom, "Equipe A")

    def test_equipe_existe(self):
        """Test de l'existence d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id_equipe": 1, "nom": "Equipe Existant"}

        # When
        result = self.equipe_service.equipe_existe(1)

        # Then
        self.assertTrue(result)

    def test_equipe_n_existe_pas(self):
        """Test de l'absence d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = None

        # When
        result = self.equipe_service.equipe_existe(999)

        # Then
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
