"""Formules du contrat de scores.

L'échelle d'une note est -10 à +10. Une note absente n'entre pas dans
la moyenne des critères. Le veto ne retire pas le candidat : il coûte
``VETO_COUT`` points par veto qui le touche.
"""

from __future__ import annotations

import numpy as np

VETO_COUT = 100.0


def satisfaction_individu(notes: list[float]) -> float:
    """Moyenne des notes connues, ou 0 s'il n'y en a aucune."""
    if not notes:
        return 0.0
    valeurs = [float(note) for note in notes]
    return sum(valeurs) / len(valeurs)


def ajuster_veto(
    satisfaction: float,
    nb_veto: int,
    veto_cout: float = VETO_COUT,
) -> float:
    """``s_i_ajuste = satisfaction - veto_cout * nb_veto``."""
    return float(satisfaction) - float(veto_cout) * int(nb_veto)


def agreger(
    satisfactions_ajustees: list[float],
    penalites: list[float],
) -> dict:
    """Agrégats d'un candidat sur l'ensemble des participants.

    ``dispersion`` est l'écart-type population (``numpy.std``, ``ddof=0``).
    ``penalite`` est la somme des pénalités individuelles.
    """
    satisfactions = [float(valeur) for valeur in satisfactions_ajustees]
    couts = [float(valeur) for valeur in penalites]
    if len(couts) != len(satisfactions):
        raise ValueError(
            "penalites et satisfactions n'ont pas la même longueur"
        )
    if not satisfactions:
        return {
            "least_misery": 0.0,
            "moyenne": 0.0,
            "penalite": 0.0,
            "dispersion": 0.0,
        }
    return {
        "least_misery": min(satisfactions),
        "moyenne": sum(satisfactions) / len(satisfactions),
        "penalite": sum(couts),
        "dispersion": float(
            np.std(np.asarray(satisfactions, dtype=float), ddof=0)
        ),
    }


def fitness_key(agregat: dict) -> tuple[float, float, float, float]:
    """Clé de tri croissant : le meilleur candidat a la plus petite clé.

    Le contrat classe par least_misery décroissant, puis moyenne
    décroissante, puis dispersion croissante, puis pénalité croissante.
    Les deux premiers critères sont donc signés moins, pour qu'un
    ``sorted(..., key=fitness_key)`` place le meilleur en tête.
    """
    return (
        -float(agregat["least_misery"]),
        -float(agregat["moyenne"]),
        float(agregat["dispersion"]),
        float(agregat["penalite"]),
    )


def entropie_round(
    fitness: list[float],
    taux_manquant: float,
) -> dict[str, float]:
    """Incertitude d'un round : ``H_classement + taux_manquant``.

    ``fitness`` contient au plus les 20 meilleures valeurs numériques
    utilisées pour l'entropie (le least_misery, critère principal :
    la fitness du contrat est un ordre lexicographique, pas un scalaire).

    ``z_k = F_k - min(F) + 1e-9``, puis ``p_k = z_k / somme(z)``,
    ``H_classement = - somme(p_k * log(p_k))`` en logarithme naturel.
    """
    taux = float(taux_manquant)
    if not fitness:
        return {"H_classement": 0.0, "taux_manquant": taux, "H_round": taux}
    valeurs = np.asarray([float(valeur) for valeur in fitness], dtype=float)
    z = valeurs - float(valeurs.min()) + 1e-9
    probabilites = z / float(z.sum())
    h_classement = float(-np.sum(probabilites * np.log(probabilites)))
    return {
        "H_classement": h_classement,
        "taux_manquant": taux,
        "H_round": h_classement + taux,
    }
