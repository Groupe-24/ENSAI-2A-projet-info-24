from unittest.mock import MagicMock
from service.tournoi_service import TournoiService
from dao.tournoi_dao import TournoiDAO


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


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
