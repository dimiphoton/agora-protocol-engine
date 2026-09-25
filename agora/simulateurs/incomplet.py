"""Profil incomplet : un masque aléatoire retire environ 40 % des notes."""

from __future__ import annotations

import random

from agora.simulateurs.commun import graine, identifiant_participant, notes_de_base

RATIO_ABSENT = 0.40


def voter(participant: dict | str, scenario: dict, seed: int = 0) -> dict:
    """Reprend la note de base et en retire une part, selon ``seed``."""
    pid = identifiant_participant(participant)
    base = notes_de_base(participant, scenario)
    rng = random.Random(graine(seed, pid))
    ordre = list(base)
    rng.shuffle(ordre)
    absents = set(ordre[: int(round(RATIO_ABSENT * len(ordre)))])
    notes = {
        identifiant: note
        for identifiant, note in base.items()
        if identifiant not in absents
    }
    return {"notes": notes, "veto": []}
