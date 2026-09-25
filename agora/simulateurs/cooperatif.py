"""Profil coopératif : notes autour du goût de groupe, sans veto."""

from __future__ import annotations

from agora.simulateurs.commun import (
    borner,
    gout_groupe,
    identifiant_participant,
    ids_domaine,
)


def voter(participant: dict | str, scenario: dict, seed: int = 0) -> dict:
    """Préférences complètes, centrées sur le goût de groupe.

    L'écart par attribut tient dans [-1, 1] : le profil reste proche
    du groupe. Aucun veto. ``seed`` ne change pas le vote, le goût de
    groupe est fixé par le scénario.
    """
    del seed
    pid = identifiant_participant(participant)
    identifiants = ids_domaine(scenario)
    groupe = gout_groupe(scenario, identifiants)
    notes = {
        identifiant: borner(
            float(groupe.get(identifiant, 0.0)) + _ecart(pid, identifiant)
        )
        for identifiant in identifiants
    }
    return {"notes": notes, "veto": []}


def _ecart(participant_id: str, identifiant: str) -> float:
    acc = 0
    for caractere in f"{participant_id}/{identifiant}":
        acc = (acc * 33 + ord(caractere)) % 997
    return (acc % 21 - 10) / 10.0
