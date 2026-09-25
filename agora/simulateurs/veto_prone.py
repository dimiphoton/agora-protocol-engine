"""Profil prompt au veto : ce qu'il rejette fortement, il le bloque."""

from __future__ import annotations

from agora.simulateurs.commun import borner, notes_de_base

# En dessous, l'attribut est un veto. Le seuil porte sur la note de base,
# avant l'abaissement des goûts négatifs.
SEUIL_VETO = -5.0
ABAISSEMENT = 2.0


def voter(participant: dict | str, scenario: dict, seed: int = 0) -> dict:
    """Notes de base, plus basses sur le négatif, veto si base < -5.

    ``seed`` ne change pas le vote : les goûts viennent du scénario.
    """
    del seed
    base = notes_de_base(participant, scenario)
    notes = {}
    veto = []
    for identifiant, note in base.items():
        if note < 0:
            notes[identifiant] = borner(note - ABAISSEMENT)
        else:
            notes[identifiant] = borner(note)
        if note < SEUIL_VETO:
            veto.append(identifiant)
    return {"notes": notes, "veto": veto}
