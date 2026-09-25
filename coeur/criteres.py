"""Critères nommés. Le veto est un coût, il ne retire pas l'option."""

from __future__ import annotations

CRITERES = ("least_misery", "moyenne")
VETO_COUT = 100.0


def evaluer(
    notes: dict[str, float | None],
    veto_par_personne: dict[str, int],
    veto_cout: float = VETO_COUT,
) -> dict[str, float]:
    """Notes par participant. Une note absente vaut 0. Le veto se soustrait."""
    if not notes:
        return {"least_misery": 0.0, "moyenne": 0.0, "penalite": 0.0}
    ajustees = []
    penalite = 0.0
    for personne, note in notes.items():
        base = 0.0 if note is None else float(note)
        cout = float(veto_cout) * int(veto_par_personne.get(personne, 0))
        ajustees.append(base - cout)
        penalite += cout
    return {
        "least_misery": min(ajustees),
        "moyenne": sum(ajustees) / len(ajustees),
        "penalite": penalite,
    }


def meilleur(scores: dict[str, dict], critere: str) -> str | None:
    """Identifiant dont le critère est le plus haut. Égalité : moyenne, puis id."""
    if critere not in CRITERES:
        raise ValueError(f"critère inconnu : {critere}")
    if not scores:
        return None
    return min(
        scores,
        key=lambda identifiant: (
            -scores[identifiant][critere],
            -scores[identifiant]["moyenne"],
            identifiant,
        ),
    )
