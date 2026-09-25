"""Un tour d'évaluation : graphe, préférences, classement, entropie."""

from __future__ import annotations

from agora.core.evaluation import evaluer_candidat
from agora.core.exploration import explorer
from agora.core.scores import entropie_round
from agora.kr.charger import charger
from agora.kr.requetes import (
    dimensions,
    etendre_preferences,
    participants,
    valeurs,
)


def tourner(scenario: dict, preferences: dict, seed: int = 0) -> dict:
    """Évalue un round et renvoie un dict sérialisable en JSON.

    ``historique`` est vide : un seul round est calculé ici.
    ``metriques`` porte les agrégats du meilleur et l'entropie du round
    (H du classement des 20 meilleurs + taux de cases manquantes).
    """
    graphe = charger(scenario)
    etendues = etendre_preferences(graphe, preferences)
    ids = [personne["id"] for personne in participants(graphe)]

    def evaluer(candidat: dict) -> dict:
        return evaluer_candidat(
            candidat,
            ids,
            etendues["notes"],
            etendues["veto"],
            graphe,
        )

    exploration = explorer(graphe, evaluer, seed=seed)
    classement = exploration["classement"]
    meilleur = exploration["meilleur"]
    taux = _taux_manquant(graphe, preferences)
    fitness = [candidat["least_misery"] for candidat in classement[:20]]
    entropie = entropie_round(fitness, taux)

    metriques = {**_agregats(meilleur), **entropie}
    return _jsonable(
        {
            "classement": classement,
            "meilleur": meilleur,
            "historique": [],
            "metriques": metriques,
            "mode": exploration["mode"],
        }
    )


def _taux_manquant(graphe, preferences: dict) -> float:
    """Cases vides / cases possibles.

    Une case est un couple (participant, valeur de dimension). Seule une
    note directe la remplit : une note héritée ne compte pas comme dite.
    """
    ids_valeurs: list[str] = []
    for dimension in dimensions(graphe):
        ids_valeurs.extend(valeurs(graphe, dimension))
    ids_personnes = [personne["id"] for personne in participants(graphe)]
    possible = len(ids_personnes) * len(ids_valeurs)
    if possible == 0:
        return 0.0
    notes = preferences.get("notes") or {}
    vides = 0
    for personne in ids_personnes:
        notes_personne = notes.get(personne) or {}
        for identifiant in ids_valeurs:
            valeur = notes_personne.get(identifiant)
            if identifiant not in notes_personne or valeur is None:
                vides += 1
    return vides / possible


def _agregats(meilleur: dict | None) -> dict:
    if not meilleur:
        return {
            "least_misery": 0.0,
            "moyenne": 0.0,
            "penalite": 0.0,
            "dispersion": 0.0,
        }
    return {
        "least_misery": meilleur["least_misery"],
        "moyenne": meilleur["moyenne"],
        "penalite": meilleur["penalite"],
        "dispersion": meilleur["dispersion"],
    }


def _jsonable(valeur):
    """Convertit les scalaires numpy et les tuples en types JSON."""
    if isinstance(valeur, dict):
        return {str(cle): _jsonable(item) for cle, item in valeur.items()}
    if isinstance(valeur, (list, tuple)):
        return [_jsonable(item) for item in valeur]
    if hasattr(valeur, "item") and callable(valeur.item):
        try:
            return _jsonable(valeur.item())
        except ValueError:
            pass
    return valeur
