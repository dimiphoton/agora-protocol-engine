"""AG qui cherche des compromis et s'arrête sur un palier d'entropie.

Génome = (destination, logement, activité). Fitness = least misery
avec pénalité de veto (échange 7), pas d'élimination dure.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product

import numpy as np
import pandas as pd

DEST = ["bretagne", "mediterranee", "auvergne"]
LOG = ["camping", "hotel", "gite"]
ACT = ["velotourisme", "festivals", "voile", "randonnee"]

# Notes échange 4 + auvergne / gite / rando interpolés
PREF: dict[str, dict[str, float]] = {
    "P1": {
        "bretagne": 10, "mediterranee": -5, "auvergne": 4,
        "camping": 8, "hotel": -2, "gite": 3,
        "velotourisme": 10, "festivals": 2, "voile": 5, "randonnee": 8,
    },
    "P2": {
        "bretagne": -5, "mediterranee": 10, "auvergne": -4,
        "camping": -10, "hotel": 10, "gite": 4,
        "velotourisme": -8, "festivals": 10, "voile": 3, "randonnee": -3,
    },
    "P3": {
        "bretagne": 5, "mediterranee": 0, "auvergne": 2,
        "camping": 3, "hotel": 5, "gite": 6,
        "velotourisme": 2, "festivals": -5, "voile": 10, "randonnee": 4,
    },
}

# Veto non-absolu : P2 refuse camping, P3 refuse festivals trop durs
VETO = {("P2", "camping"): 1.0, ("P3", "festivals"): 0.7}
VETO_PENALITE = 25.0

Genome = tuple[str, str, str]


def shannon_from_counts(counts: list[int]) -> float:
    total = sum(counts)
    if total == 0:
        return 0.0
    p = np.array(counts, dtype=float) / total
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p))) + 0.0


def scores_individuels(g: Genome) -> dict[str, float]:
    dest, log, act = g
    out = {}
    for p, notes in PREF.items():
        s = notes[dest] + notes[log] + notes[act]
        for (pp, option), intensite in VETO.items():
            if pp == p and option in g:
                s -= VETO_PENALITE * intensite
        out[p] = s
    return out


def least_misery(g: Genome) -> float:
    return min(scores_individuels(g).values())


def h_clause(g: Genome) -> float:
    """Entropie : les 3 participants sont-ils du même côté du zéro ?"""
    sc = list(scores_individuels(g).values())
    urnes = [sum(1 for s in sc if s < 0), sum(1 for s in sc if s == 0), sum(1 for s in sc if s > 0)]
    return shannon_from_counts(urnes)


def h_population(pop: list[Genome]) -> float:
    c = Counter(pop)
    return shannon_from_counts(list(c.values()))


def exhaustif() -> tuple[Genome, float]:
    best_g, best_f = None, -1e9
    for g in product(DEST, LOG, ACT):
        f = least_misery(g)
        if f > best_f:
            best_g, best_f = g, f
    assert best_g is not None
    return best_g, best_f


@dataclass
class Hist:
    gen: int
    best_f: float
    mean_f: float
    h_pop: float
    h_best: float


def tournoi(pop: list[Genome], rng: np.random.Generator) -> Genome:
    a, b = pop[int(rng.integers(len(pop)))], pop[int(rng.integers(len(pop)))]
    return a if least_misery(a) >= least_misery(b) else b


def croiser(a: Genome, b: Genome, rng: np.random.Generator) -> Genome:
    return tuple(a[i] if rng.random() < 0.5 else b[i] for i in range(3))  # type: ignore[return-value]


def muter(g: Genome, rng: np.random.Generator, p: float = 0.2) -> Genome:
    alleles = [DEST, LOG, ACT]
    out = list(g)
    for i, choix in enumerate(alleles):
        if rng.random() < p:
            out[i] = str(choix[int(rng.integers(len(choix)))])
    return (out[0], out[1], out[2])


def run_ga(
    n_pop: int = 40,
    n_gen: int = 80,
    patience: int = 8,
    eps: float = 1e-6,
    seed: int = 0,
) -> tuple[Genome, list[Hist], int]:
    rng = np.random.default_rng(seed)
    pop = [
        (str(DEST[i]), str(LOG[j]), str(ACT[k]))
        for i, j, k in rng.integers(
            [len(DEST), len(LOG), len(ACT)], size=(n_pop, 3)
        )
    ]
    hist: list[Hist] = []
    plateau_at = n_gen
    for gen in range(n_gen):
        fits = [least_misery(g) for g in pop]
        best_i = int(np.argmax(fits))
        rec = Hist(
            gen=gen,
            best_f=float(fits[best_i]),
            mean_f=float(np.mean(fits)),
            h_pop=h_population(pop),
            h_best=h_clause(pop[best_i]),
        )
        hist.append(rec)
        if gen >= patience:
            fenetre = hist[-patience:]
            df = np.std([h.best_f for h in fenetre])
            dh = np.std([h.h_best for h in fenetre])
            if df < eps and dh < 0.05:
                plateau_at = gen
                break
        nouvelle: list[Genome] = [pop[best_i]]  # elitisme
        while len(nouvelle) < n_pop:
            enfant = muter(croiser(tournoi(pop, rng), tournoi(pop, rng), rng), rng)
            nouvelle.append(enfant)
        pop = nouvelle
    best = max(pop, key=least_misery)
    return best, hist, plateau_at


def main() -> None:
    opt, opt_f = exhaustif()
    best, hist, palier = run_ga()
    print("=== AG + paliers d'entropie — vacances 3×3×4 = 36 génomes ===")
    print(f"Optimum exhaustif : {opt}  least_misery={opt_f:.1f}")
    print(f"Meilleur AG       : {best}  least_misery={least_misery(best):.1f}")
    print(f"Scores AG : {scores_individuels(best)}")
    print(f"Palier à la génération {palier} / dernière {hist[-1].gen}")
    print(f"H_pop final={hist[-1].h_pop:.3f}  H_best={hist[-1].h_best:.3f}")
    print(f"gap_vs_exhaustif = {opt_f - least_misery(best):.3f}")
    df = pd.DataFrame([h.__dict__ for h in hist])
    print("\nCourbe (chaque  max(1, n/8) gens) :")
    step = max(1, len(df) // 8)
    print(df.iloc[::step][["gen", "best_f", "mean_f", "h_pop", "h_best"]].round(3).to_string(index=False))
    print("\nMétriques :")
    print(f"  best_least_misery: {least_misery(best):.3f}")
    print(f"  opt_least_misery: {opt_f:.3f}")
    print(f"  generation_palier: {palier}")
    print(f"  H_pop_final: {hist[-1].h_pop:.3f}")
    print(f"  H_best_final: {hist[-1].h_best:.3f}")
    print(f"  gap_vs_exhaustif: {opt_f - least_misery(best):.3f}")
    print(f"  n_generations_run: {hist[-1].gen + 1}")
    print(
        "\nLecture : le palier arrête l'AG quand fitness ET entropie du "
        "meilleur stagnent. gap=0 ici (espace minuscule) : l'AG n'est pas "
        "nécessaire au MVP vacances, il le devient dès que le génome s'allonge."
    )


if __name__ == "__main__":
    main()
