"""Évalue et classe des candidats déjà construits."""

from __future__ import annotations

import networkx as nx

from agora.core.scores import (
    VETO_COUT,
    agreger,
    ajuster_veto,
    fitness_key,
    satisfaction_individu,
)
from agora.kr.requetes import compter_veto


def evaluer_candidat(
    candidat: dict,
    participants: list,
    preferences_etendues: dict,
    veto: dict | None = None,
    graphe: nx.MultiDiGraph | None = None,
    veto_cout: float = VETO_COUT,
) -> dict:
    """Agrégats du candidat et détail par personne.

    ``preferences_etendues`` est ``{personne: {attribut: note}}`` (les notes
    déjà héritées). ``veto`` est ``{personne: [attribut, ...]}``.
    Une note absente ne compte pas dans la moyenne de la personne.
    Un veto qui touche le choix pénalise, il ne retire pas le candidat.
    """
    veto = veto or {}
    choix = candidat.get("choix") or {}
    ids = _ids_participants(participants)

    detail = {}
    satisfactions = []
    penalites = []
    for personne in ids:
        notes_personne = preferences_etendues.get(personne) or {}
        notes = []
        for attribut in choix.values():
            if attribut not in notes_personne:
                continue
            valeur = notes_personne[attribut]
            if valeur is None:
                continue
            notes.append(float(valeur))
        satisfaction = satisfaction_individu(notes)
        nb_veto = compter_veto(graphe, choix, list(veto.get(personne) or []))
        penalite = float(veto_cout) * nb_veto
        ajustee = ajuster_veto(satisfaction, nb_veto, veto_cout)
        detail[personne] = {
            "notes": notes,
            "satisfaction": satisfaction,
            "nb_veto": nb_veto,
            "penalite": penalite,
            "satisfaction_ajustee": ajustee,
        }
        satisfactions.append(ajustee)
        penalites.append(penalite)

    agregat = agreger(satisfactions, penalites)
    agregat["detail"] = detail
    return agregat


def classer(
    candidats: list[dict],
    participants: list,
    preferences_etendues: dict,
    veto: dict | None = None,
    graphe: nx.MultiDiGraph | None = None,
    veto_cout: float = VETO_COUT,
) -> list[dict]:
    """Du meilleur au moins bon. Un candidat vetoé reste dans la liste."""
    classes = []
    for candidat in candidats:
        agregat = evaluer_candidat(
            candidat,
            participants,
            preferences_etendues,
            veto,
            graphe,
            veto_cout,
        )
        classes.append({**candidat, **agregat})
    classes.sort(key=fitness_key)
    return classes


def _ids_participants(participants: list) -> list[str]:
    ids = []
    for participant in participants:
        if isinstance(participant, str):
            ids.append(participant)
        else:
            ids.append(participant["id"])
    return ids
