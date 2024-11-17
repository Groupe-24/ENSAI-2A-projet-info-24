from unittest.mock import MagicMock
from service.pari_service import PariService
from dao.pari_dao import PariDAO
import pytest


def test_parier():
    """Test de la création d'un pari"""

    # GIVEN
    pari_dao_mock = PariDAO()
    pari_dao_mock.insert_pari = MagicMock()
    pari_service = PariService(pari_dao_mock)

    # Création des mocks pour match, équipe et utilisateur avec les attributs nécessaires
    match_mock = MagicMock()
    match_mock.id_match = "1"

    equipe_mock = MagicMock()
    equipe_mock.id_equipe = "10"

    utilisateur_mock = MagicMock()
    utilisateur_mock.id_utilisateur = "100"

    # WHEN
    pari = pari_service.parier(
        match=match_mock, equipe=equipe_mock, utilisateur=utilisateur_mock, mise=150, gain=None
    )

    # THEN
    assert pari.id_pari is not None
    assert pari.mise == 150
    pari_dao_mock.insert_pari.assert_called_once_with(
        id_pari=pari.id_pari,
        id_match="1",  # Utilisation de l'id de match défini dans le mock
        id_equipe="10",  # Utilisation de l'id d'équipe défini dans le mock
        id_utilisateur="100",  # Utilisation de l'id utilisateur défini dans le mock
        mise=150,
        gain=None,
    )


def test_afficher_cote(capsys):
    """Test de la méthode afficher_cote"""

    # GIVEN:
    pari_dao_mock = MagicMock(PariDAO)
    pari_service = PariService(pari_dao_mock)

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

    # MOCK:
    pari_dao_mock.list_pari_match.return_value = resultat_paris

    # WHEN:
    result = pari_service.afficher_cote(match_mock)

    # THEN:
    cote_equipe_bleu = (100 + 50) / (100 + 50 + 150)
    cote_equipe_orange = 150 / (100 + 50 + 150)

    assert result["match"] == "101"
    assert result["1"] == "bleu"
    assert result["2"] == "orange"
    assert result["cote_equipe_bleu"] == cote_equipe_bleu
    assert result["cote_equipe_orange"] == cote_equipe_orange

    pari_dao_mock.list_pari_match.assert_called_once_with("101")

    expected_output = (
        f"Cote equipe bleu : {cote_equipe_bleu}\nCote equipe orange : {cote_equipe_orange}\n"
    )

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_gain_potentiel():
    """Test de la méthode gain_potentiel"""

    # Test 1: Erreur d'une équipe qui ne fait pas partie du match
    # GIVEN:
    pari_dao_mock = MagicMock(PariDAO)
    pari_service = PariService(pari_dao_mock)

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
    with pytest.raises(ValueError, match="L'équipe doit jouer dans le match spécifié."):
        pari_service.gain_potentiel(100, equipe_mock, match_mock)

    # Test 2 : Cas classique
    # GIVEN
    cotes_mock = {
        "match": "101",
        "1": "bleu",
        "2": "orange",
        "cote_equipe_bleu": 1.5,
        "cote_equipe_orange": 2.0,
    }
    pari_service.afficher_cote = MagicMock(return_value=cotes_mock)

    # WHEN:
    mise = 100
    gain_potentiel = pari_service.gain_potentiel(mise, equipe_bleu_mock, match_mock)

    # THEN:
    # (cote_equipe_bleu + 1) * mise
    expected_gain = (1.5 + 1) * mise  # 2.5 * 100 = 250

    assert gain_potentiel == expected_gain
    pari_service.afficher_cote.assert_called_once_with(match_mock)


def test_supprimer_pari(capsys):
    """Test de la méthode supprimer_pari pour un pari existant et inexistant"""

    # Test 1 : Pari Existant
    # GIVEN:
    pari_dao_mock = MagicMock()
    pari_service = PariService(pari_dao_mock)

    pari_mock = MagicMock()
    pari_mock.id_pari = "123"

    pari_dao_mock.exists_by_id.return_value = True

    # WHEN:
    pari_service.supprimer_pari(pari_mock)

    # THEN:
    pari_dao_mock.exists_by_id.assert_called_once_with("123")
    pari_dao_mock.delete_pari.assert_called_once_with("123")
    captured = capsys.readouterr()
    assert captured.out == "Le pari a bien été supprimé.\n"

    # Test 2 : Pari inexistant
    # GIVEN:
    pari_dao_mock.reset_mock()
    pari_dao_mock.exists_by_id.return_value = False

    # WHEN:
    pari_service.supprimer_pari(pari_mock)

    # THEN:
    pari_dao_mock.exists_by_id.assert_called_once_with("123")
    pari_dao_mock.delete_pari.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == "Le pari n'existe pas.\n"


if __name__ == "__main__":
    pytest.main([__file__])
