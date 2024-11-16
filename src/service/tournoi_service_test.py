from unittest.mock import MagicMock
from service.tournoi_service import TournoiService
from dao.tournoi_dao import TournoiDAO
from business_object.tournoi import Tournoi


def test_creer_tournoi():
    """Test de la création d'un tournoi"""

    # GIVEN
    tournoi_dao_mock = TournoiDAO()
    tournoi_dao_mock.insert_tournoi = MagicMock()

    organisateur_mock = MagicMock()
    organisateur_mock.pseudo = "organisateur_test"

    tournoi_service = TournoiService(tournoi_dao_mock)

    # WHEN
    tournoi = tournoi_service.creer_tournoi(
        titre="Tournoi Test",
        description="Description du tournoi",
        date_debut="2024-01-01",
        date_fin="2024-01-02",
        organisateur=organisateur_mock,
    )

    # THEN
    assert tournoi.id_tournoi is not None
    assert tournoi.titre == "Tournoi Test"
    assert tournoi.description == "Description du tournoi"
    assert tournoi.date_debut == "2024-01-01"
    assert tournoi.date_fin == "2024-01-02"
    assert tournoi.organisateur == "organisateur_test"
    tournoi_dao_mock.insert_tournoi.assert_called_once_with(
        id_tournoi=tournoi.id_tournoi,
        titre="Tournoi Test",
        description="Description du tournoi",
        date_debut="2024-01-01",
        date_fin="2024-01-02",
        organisateur="organisateur_test",
    )


def test_lister_tournois():
    """Test de la liste des tournois"""

    # GIVEN
    tournoi_dao_mock = TournoiDAO()
    tournoi_dao_mock.list_tournois = MagicMock(
        return_value=[
            {
                "id_tournoi": "1",
                "titre": "Tournoi 1",
                "description": "Description 1",
                "date_debut": "2024-01-01",
                "date_fin": "2024-01-02",
                "id_organisateur": "organisateur_1",
            }
        ]
    )

    tournoi_service = TournoiService(tournoi_dao_mock)

    # WHEN
    result = tournoi_service.lister_tournois()

    # THEN
    assert len(result) == 1
    assert result[0].id_tournoi == "1"
    assert result[0].titre == "Tournoi 1"
    assert result[0].description == "Description 1"


def test_rechercher_tournoi_nom():
    """Test de la recherche d'un tournoi par nom"""

    # GIVEN
    tournoi_dao_mock = TournoiDAO()
    tournoi_dao_mock.tournoi_par_nom = MagicMock(
        return_value=[
            {
                "id_tournoi": "2",
                "titre": "Tournoi Recherche",
                "description": "Description Recherche",
                "date_debut": "2024-01-03",
                "date_fin": "2024-01-04",
                "id_organisateur": "organisateur_2",
            }
        ]
    )

    tournoi_service = TournoiService(tournoi_dao_mock)

    # WHEN
    result = tournoi_service.rechercher_tournoi_nom("Recherche")

    # THEN
    assert len(result) == 1
    assert result[0].titre == "Tournoi Recherche"
    assert result[0].id_tournoi == "2"


def test_supprimer_tournoi():
    """Test de la suppression d'un tournoi"""

    # Test 1 : tournoi existant
    # GIVEN
    tournoi_dao_mock = MagicMock(TournoiDAO)
    tournoi_dao_mock.get_tournoi_by_id = MagicMock(
        return_value={"id_tournoi": "1", "titre": "Tournoi 1"}
    )
    tournoi_dao_mock.delete_tournoi = MagicMock()

    organisateur_mock = MagicMock()
    organisateur_mock.pseudo = "organisateur_test"

    tournoi_service = TournoiService(tournoi_dao_mock)
    tournoi = Tournoi(
        id_tournoi="1",
        titre="Tournoi Test",
        description="Description du tournoi",
        date_debut="2024-01-01",
        date_fin="2024-01-02",
        organisateur=organisateur_mock,
    )

    # WHEN
    resultat = tournoi_service.supprimer_tournoi(tournoi)

    # THEN
    assert resultat == "Le tournoi a bien été supprimé."
    tournoi_dao_mock.delete_tournoi.assert_called_once_with("1")

    # Réinitialiser les mocks pour le second test
    tournoi_dao_mock.reset_mock()

    # Test 2 : tournoi inexistant
    # GIVEN
    tournoi_dao_mock.get_tournoi_by_id = MagicMock(return_value=None)
    tournoi_service = TournoiService(tournoi_dao_mock)

    # Créer un tournoi avec un ID fictif
    tournoi = Tournoi(
        id_tournoi="999",
        titre="Tournoi Inexistant",
        description="Description du tournoi",
        date_debut="2024-01-01",
        date_fin="2024-01-02",
        organisateur=organisateur_mock,
    )

    # WHEN
    resultat = tournoi_service.supprimer_tournoi(tournoi)

    # THEN
    assert resultat == "Le tournoi spécifié n'existe pas."

    # Vérifier que delete_tournoi n'a pas été appelé dans ce cas
    tournoi_dao_mock.delete_tournoi.assert_not_called()


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
