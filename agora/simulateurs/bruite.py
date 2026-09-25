"""Profil bruité : bruit gaussien d'écart-type 2, borné à [-10, 10]."""

from __future__ import annotations

import random

from agora.simulateurs.commun import (
    borner,
    graine,
    identifiant_participant,
    notes_de_base,
)

ECART_TYPE = 2.0


def voter(participant: dict | str, scenario: dict, seed: int = 0) -> dict:
    """Ajoute un bruit gaussien à chaque note de base. Pas de veto."""
    pid = identifiant_participant(participant)
    base = notes_de_base(participant, scenario)
    rng = random.Random(graine(seed, pid))
    notes = {
        identifiant: borner(note + rng.gauss(0.0, ECART_TYPE))
        for identifiant, note in base.items()
    }
    return {"notes": notes, "veto": []}
