from unittest.mock import MagicMock
from service.joueur_service import JoueurService


def test_rechercher_joueur_trouve():
    """Test de la recherche d'un joueur avec un pseudo existant"""

    # GIVEN
    pseudo = "jp"
    joueur_dao_mock = MagicMock()
    joueur_dao_mock.get_joueur_by_parameters.return_value = [
        {"id_joueurs": 1, "pseudo": "jp", "equipe": "Equipe1", "professionnel": True}
    ]

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
    joueur_dao_mock = MagicMock()
    joueur_dao_mock.get_joueur_by_parameters.return_value = []

    joueur_service = JoueurService(joueur_dao_mock)

    # WHEN
    result = joueur_service.rechercher_joueur(pseudo)

    # THEN
    assert len(result) == 0


def test_creer_joueur_succes():
    """Test de la création d'un joueur avec succès"""

    # GIVEN
    joueur_dao_mock = MagicMock()
    joueur_service = JoueurService(joueur_dao_mock)
    joueur_dao_mock.exists_by_id.return_value = False
    joueur_dao_mock.get_joueur_by_parameters.return_value = None

    # WHEN
    result = joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

    # THEN
    assert result == "Le joueur 'PseudoTest' a été créé avec succès."
    joueur_dao_mock.insert_joueur.assert_called_once_with(
        id_joueur=1, pseudo="PseudoTest", equipe="EquipeTest", professionnel=True
    )


class TestJoueurServiceWithSelf:
    """Tests nécessitant une configuration avec `self`"""

    def setup_method(self):
        """Initialise les mocks avant chaque test"""
        self.joueur_dao = MagicMock()
        self.joueur_service = JoueurService(self.joueur_dao)

    def test_creer_joueur_pseudo_existant(self):
        """Test pour vérifier qu'un joueur avec un pseudo existant ne peut pas être créé"""

        # GIVEN
        self.joueur_dao.exists_by_id.return_value = False
        self.joueur_dao.get_joueur_by_parameters.return_value = [{"pseudo": "PseudoTest"}]

        # WHEN
        result = self.joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

        # THEN
        assert result == "Un joueur avec le pseudo 'PseudoTest' existe déjà."
        self.joueur_dao.insert_joueur.assert_not_called()

    def test_creer_joueur_id_existant(self):
        """Test pour vérifier qu'un joueur avec un ID existant ne peut pas être créé"""

        # GIVEN
        self.joueur_dao.exists_by_id.return_value = True

        # WHEN
        result = self.joueur_service.creer_joueur(1, "PseudoTest", "EquipeTest", True)

        # THEN
        assert result == "Un joueur avec l'ID 1 existe déjà."
        self.joueur_dao.insert_joueur.assert_not_called()


def test_supprimer_joueur_succes():
    """Test de la suppression réussie d'un joueur existant"""

    # GIVEN
    joueur_dao_mock = MagicMock()
    joueur_service = JoueurService(joueur_dao_mock)
    joueur_dao_mock.exists_by_id.return_value = True

    # WHEN
    result = joueur_service.supprimer_joueur(1)

    # THEN
    assert result == "Le joueur avec l'ID 1 a été supprimé avec succès."
    joueur_dao_mock.delete_joueur.assert_called_once_with(1)


def test_supprimer_joueur_inexistant():
    """Test de la suppression d'un joueur inexistant"""

    # GIVEN
    joueur_dao_mock = MagicMock()
    joueur_service = JoueurService(joueur_dao_mock)
    joueur_dao_mock.exists_by_id.return_value = False

    # WHEN
    result = joueur_service.supprimer_joueur(1)

    # THEN
    assert result == "Le joueur avec l'ID 1 n'existe pas."
    joueur_dao_mock.delete_joueur.assert_not_called()


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
