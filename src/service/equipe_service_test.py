import unittest
from unittest.mock import MagicMock
from service.equipe_service import EquipeService


class TestEquipeService(unittest.TestCase):
    def setUp(self):
        self.equipeDao = MagicMock()
        self.equipe_service = EquipeService(self.equipeDao)

    def test_lister_equipes(self):
        """Test de la liste de toutes les équipes"""
        # Given
        self.equipeDao.list_equipes.return_value = ["Equipe 1", "Equipe 2"]

        # When
        result = self.equipe_service.lister_equipes()

        # Then
        self.assertEqual(result, ["Equipe 1", "Equipe 2"])

    def test_rechercher_equipe_existe(self):
        """Test de la recherche d'une équipe existante selon l'id"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id": 1, "nom": "Equipe 1"}

        # When
        result = self.equipe_service.rechercher_equipe(1)

        # Then
        self.assertEqual(result, {"id": 1, "nom": "Equipe 1"})

    def test_rechercher_equipe_n_existe_pas(self):
        """Test de la recherche d'une équipe inexistante selon l'id"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = None

        # When
        result = self.equipe_service.rechercher_equipe(999)

        # Then
        self.assertEqual(result, "Il n'y a pas d'équipe avec cet ID.")

    def test_ajouter_equipe(self):
        """Test d'ajout d'une équipe"""
        # Given
        self.equipeDao.insert_equipe.return_value = True

        # When
        result = self.equipe_service.ajouter_equipe("Nouvelle Equipe", "Description de l'équipe")

        # Then
        self.assertTrue(result)
        self.equipeDao.insert_equipe.assert_called_once_with(
            "Nouvelle Equipe", "Description de l'équipe"
        )

    def test_modifier_equipe(self):
        """Test de modification d'une information d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {
            "id": 1,
            "nom": "Ancienne Equipe",
            "description": "Ancienne description",
        }

        # When
        result = self.equipe_service.modifier_equipe(1, nom="Nouvelle Equipe")

        # Then
        self.assertEqual(result["nom"], "Nouvelle Equipe")
        self.equipeDao.update_equipe.assert_called_once_with(result)

    def test_supprimer_equipe(self):
        """Test de suppression d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id": 1, "nom": "Equipe à supprimer"}

        # When
        result = self.equipe_service.supprimer_equipe(1)

        # Then
        self.assertEqual(result, "Équipe supprimée avec succès")
        self.equipeDao.delete_equipe.assert_called_once_with(1)

    def test_lister_equipes_par_nom(self):
        """Test de la liste d'équipes selon le nom"""
        # Given
        self.equipeDao.list_equipes_by_name.return_value = ["Equipe A", "Equipe B"]

        # When
        result = self.equipe_service.lister_equipes_par_nom("Equipe")

        # Then
        self.assertEqual(result, ["Equipe A", "Equipe B"])

    def test_lister_equipes_par_tournoi(self):
        """Test de la liste d'équipes selon le tournoi"""
        # Given
        self.equipeDao.list_equipes_by_tournament.return_value = ["Equipe A", "Equipe B"]

        # When
        result = self.equipe_service.lister_equipes_par_tournoi(1)

        # Then
        self.assertEqual(result, ["Equipe A", "Equipe B"])

    def test_equipe_existe(self):
        """Test de l'existance d'une équipe"""
        # Given
        self.equipeDao.get_equipe_by_id.return_value = {"id": 1, "nom": "Equipe Existant"}

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
