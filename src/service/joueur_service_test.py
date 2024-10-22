from unittest.mock import MagicMock
from service.joueur_service import JoueurService
from dao.joueur_dao import JoueursDAO


def test_rechercher_joueur_trouve():
    """Test de la recherche d'un joueur avec un pseudo existant"""

    # GIVEN
    pseudo = "jp"
    joueur_dao_mock = JoueursDAO()

    # Simulation du retour de la méthode `get_joueur_by_parameters` de JoueursDAO
    joueur_dao_mock.get_joueur_by_parameters = MagicMock(
        return_value=[
            {
                "id_joueurs": 1,
                "pseudo": "jp",
                "equipe": "Equipe1",
                "professionnel": True,
            }
        ]
    )

    # Création du service avec le mock
    joueur_service = JoueurService(joueur_dao_mock)

    # WHEN
    result = joueur_service.rechercher_joueur(pseudo)

    # THEN
    assert len(result) == 1
    assert result[0].pseudo == "jp"
    assert result[0].equipe == "Equipe1"
    assert result[0].professionnel is True


def test_rechercher_joueur_non_trouve():
    """Test de la recherche d'un joueur avec un pseudo inexistant"""

    # GIVEN
    pseudo = "inexistant"
    joueur_dao_mock = JoueursDAO()

    # Simulation d'un retour vide pour un pseudo qui n'existe pas
    joueur_dao_mock.get_joueur_by_parameters = MagicMock(return_value=[])

    # Création du service avec le mock
    joueur_service = JoueurService(joueur_dao_mock)

    # WHEN
    result = joueur_service.rechercher_joueur(pseudo)

    # THEN
    assert len(result) == 0


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
