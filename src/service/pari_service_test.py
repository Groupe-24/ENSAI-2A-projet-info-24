from unittest.mock import MagicMock
from service.pari_service import PariService
from dao.pari_dao import PariDAO
from business_object.pari import Pari
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

    # GIVEN: Création des mocks pour les objets nécessaires
    pari_dao_mock = MagicMock(PariDAO)
    pari_service = PariService(pari_dao_mock)

    # Création d'un match mocké avec les équipes
    equipe_bleu_mock = MagicMock()
    equipe_bleu_mock.id_equipe = "1"

    equipe_orange_mock = MagicMock()
    equipe_orange_mock.id_equipe = "2"

    match_mock = MagicMock()
    match_mock.id_match = "101"
    match_mock.equipe_bleu = equipe_bleu_mock
    match_mock.equipe_orange = equipe_orange_mock

    # Données simulées pour les paris
    resultat_paris = [
        {"id_equipe": "1", "mise": 100},  # Pari sur l'équipe bleue
        {"id_equipe": "2", "mise": 150},  # Pari sur l'équipe orange
        {"id_equipe": "1", "mise": 50},  # Autre pari sur l'équipe bleue
    ]

    # MOCK: La méthode liste_pari_match renvoie les paris simulés
    pari_dao_mock.list_pari_match.return_value = resultat_paris

    # WHEN: Appel à la fonction afficher_cote
    result = pari_service.afficher_cote(match_mock)

    # THEN: Vérification des calculs des cotes
    cote_equipe_bleu = (100 + 50) / (100 + 50 + 150)
    cote_equipe_orange = 150 / (100 + 50 + 150)

    # Vérifications du retour de la fonction
    assert result["match"] == "101"
    assert result["1"] == "bleu"
    assert result["2"] == "orange"
    assert result["cote_equipe_bleu"] == cote_equipe_bleu
    assert result["cote_equipe_orange"] == cote_equipe_orange

    # Vérification de l'appel à la méthode liste_pari_match
    pari_dao_mock.list_pari_match.assert_called_once_with("101")

    # Vérification de l'affichage des cotes via capsys
    expected_output = (
        f"Cote equipe bleu : {cote_equipe_bleu}\nCote equipe orange : {cote_equipe_orange}\n"
    )

    # Utilisation de capsys pour capturer stdout
    captured = capsys.readouterr()  # Récupère ce qui a été imprimé dans la sortie
    assert (
        captured.out == expected_output
    )  # Vérifie que la sortie capturée correspond à ce que l'on attend


def test_gain_potentiel():
    """Test de la méthode gain_potentiel"""

    # GIVEN: Création des mocks pour les objets nécessaires
    pari_dao_mock = MagicMock(PariDAO)
    pari_service = PariService(pari_dao_mock)

    # Création d'une équipe mockée
    equipe_bleu_mock = MagicMock()
    equipe_bleu_mock.id_equipe = "1"

    equipe_orange_mock = MagicMock()
    equipe_orange_mock.id_equipe = "2"

    # Création d'un match mocké avec les équipes
    match_mock = MagicMock()
    match_mock.id_match = "101"
    match_mock.equipe_bleu = equipe_bleu_mock
    match_mock.equipe_orange = equipe_orange_mock

    # Données simulées pour les cotes retournées par afficher_cote
    cotes_simulees = {
        "match": "101",
        "1": "bleu",  # L'équipe bleue a la clé "1"
        "2": "orange",  # L'équipe orange a la clé "2"
        "cote_equipe_bleu": 1.5,  # Cote de l'équipe bleue
        "cote_equipe_orange": 2.0,  # Cote de l'équipe orange
    }

    # MOCK: La méthode afficher_cote renvoie les cotes simulées
    pari_service.afficher_cote = MagicMock(return_value=cotes_simulees)

    # WHEN: Appel à la fonction gain_potentiel pour l'équipe bleue avec une mise de 100
    mise = 100
    result_bleu = pari_service.gain_potentiel(mise, equipe_bleu_mock, match_mock)

    # WHEN: Appel à la fonction gain_potentiel pour l'équipe orange avec une mise de 100
    result_orange = pari_service.gain_potentiel(mise, equipe_orange_mock, match_mock)

    # THEN: Vérification du calcul du gain potentiel
    # Pour l'équipe bleue: (1.5 + 1) * 100 = 250
    assert result_bleu == 250

    # Pour l'équipe orange: (2.0 + 1) * 100 = 300
    assert result_orange == 300

    # Vérification que afficher_cote a bien été appelé pour obtenir les cotes
    # Ici nous permettons 2 appels à la méthode afficher_cote
    pari_service.afficher_cote.assert_any_call(match_mock)
    assert pari_service.afficher_cote.call_count == 2


def test_supprimer_pari():
    """Test de la méthode supprimer_pari"""

    # GIVEN: Création des mocks pour les objets nécessaires
    pari_dao_mock = MagicMock(PariDAO)
    pari_service = PariService(pari_dao_mock)

    # Création d'un pari mocké
    pari_mock = MagicMock(Pari)
    pari_mock.id_pari = "12345"

    # Test 1: Le pari existe
    # MOCK: La méthode exists_by_id renvoie True (le pari existe)
    pari_dao_mock.exists_by_id.return_value = True

    # WHEN: Appel à la fonction supprimer_pari pour un pari existant
    result = pari_service.supprimer_pari(pari_mock)

    # THEN: Vérification du message de succès
    assert result == "Le pari a bien été supprimé."

    # Vérification que la méthode delete_pari a bien été appelée
    pari_dao_mock.delete_pari.assert_called_once_with(pari_mock.id_pari)

    # Reset mocks
    pari_dao_mock.reset_mock()

    # Test 2: Le pari n'existe pas
    # MOCK: La méthode exists_by_id renvoie False (le pari n'existe pas)
    pari_dao_mock.exists_by_id.return_value = False

    # WHEN: Appel à la fonction supprimer_pari pour un pari qui n'existe pas
    result_non_existant = pari_service.supprimer_pari(pari_mock)

    # THEN: Vérification du message d'erreur
    assert result_non_existant == "Le pari n'existe pas."

    # Vérification que la méthode delete_pari n'a pas été appelée dans ce cas
    pari_dao_mock.delete_pari.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__])
