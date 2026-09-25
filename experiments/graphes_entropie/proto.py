"""Résumé mathématique : graphe de positions + entropie de désaccord.

Notes -10..+10 reprises de l'échange 4 (MVP vacances).
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd

NOTES = pd.DataFrame(
    {
        "bretagne": [10, -5, 5],
        "mediterranee": [-5, 10, 0],
        "camping": [8, -10, 3],
        "hotel": [-2, 10, 5],
        "velotourisme": [10, -8, 2],
        "festivals": [2, 10, -5],
        "voile": [5, 3, 10],
    },
    index=["P1", "P2", "P3"],
)

DIMENSIONS = {
    "destination": ["bretagne", "mediterranee"],
    "logement": ["camping", "hotel"],
    "activite": ["velotourisme", "festivals", "voile"],
}

POIDS = {"destination": 1.0, "logement": 1.0, "activite": 1.2}


def shannon(p: np.ndarray) -> float:
    p = p[p > 0]
    if p.size == 0:
        return 0.0
    return float(-np.sum(p * np.log2(p)))


def votes_discrets(col: pd.Series) -> np.ndarray:
    """Trois urnes : contre (<0), neutre (0), pour (>0)."""
    counts = np.array(
        [(col < 0).sum(), (col == 0).sum(), (col > 0).sum()],
        dtype=float,
    )
    total = counts.sum()
    return counts / total if total else counts


def entropie_option(col: pd.Series) -> float:
    return shannon(votes_discrets(col))


def entropie_dimension(df: pd.DataFrame, options: list[str]) -> float:
    """Entropie moyenne des options de la dimension, plus désaccord de ranking."""
    h_opts = np.mean([entropie_option(df[o]) for o in options])
    # Qui est le favori de chacun ? si tous le même, H_rank = 0
    favoris = df[options].idxmax(axis=1)
    vc = favoris.value_counts(normalize=True).reindex(options, fill_value=0).to_numpy(dtype=float)
    return 0.5 * h_opts + 0.5 * shannon(vc)


def h_cons(df: pd.DataFrame) -> tuple[dict[str, float], float]:
    h_dim = {dim: entropie_dimension(df, opts) for dim, opts in DIMENSIONS.items()}
    num = sum(POIDS[d] * h for d, h in h_dim.items())
    den = sum(POIDS.values())
    return h_dim, num / den


def graphe_positions(df: pd.DataFrame) -> pd.DataFrame:
    """Distance L1 moyenne entre participants (notes normalisées / 10)."""
    names = list(df.index)
    mat = pd.DataFrame(0.0, index=names, columns=names)
    for i, j in combinations(names, 2):
        d = float(np.mean(np.abs(df.loc[i] - df.loc[j]) / 10.0))
        mat.loc[i, j] = d
        mat.loc[j, i] = d
    return mat


def ascii_graphe(mat: pd.DataFrame) -> str:
    lines = ["  graphe (épaisseur ~ désaccord) :"]
    for i, j in combinations(mat.index, 2):
        d = mat.loc[i, j]
        bar = "█" * int(round(d * 20))
        lines.append(f"    {i} —— {j}  {d:.2f}  {bar}")
    return "\n".join(lines)


def question_max_gain(df: pd.DataFrame) -> tuple[str, float]:
    """Élicitation active : quelle dimension, si figée, baisserait le plus H_cons ?"""
    _, h0 = h_cons(df)
    best_dim, best_gain = "", -1.0
    for dim, opts in DIMENSIONS.items():
        # on « clarifie » en collapsant chaque participant sur son max
        sim = df.copy()
        for p in sim.index:
            fav = sim.loc[p, opts].idxmax()
            for o in opts:
                sim.loc[p, o] = 10 if o == fav else -10
        _, h1 = h_cons(sim)
        gain = h0 - h1
        if gain > best_gain:
            best_dim, best_gain = dim, gain
    return best_dim, best_gain


def choc_veto(df: pd.DataFrame) -> pd.DataFrame:
    """P2 refuse soudain la voile (seul quasi-consensus). H peut remonter."""
    out = df.copy()
    out.loc["P2", "voile"] = -10
    return out


def main() -> None:
    print("=== Graphes & entropie — notes de l'échange 4 ===")
    print(NOTES.to_string())
    h_dim, h0 = h_cons(NOTES)
    print("\nEntropie par dimension :")
    for d, h in h_dim.items():
        print(f"  H({d}) = {h:.3f} bits  (poids {POIDS[d]})")
    print(f"  H_cons = {h0:.3f} bits")
    dim, gain = question_max_gain(NOTES)
    print(f"\nProchaine question (max ΔH) : sondage sur « {dim} »  gain≈{gain:.3f}")
    mat = graphe_positions(NOTES)
    print("\nMatrice de désaccord (L1/10) :")
    print(mat.round(3).to_string())
    print(ascii_graphe(mat))
    after = choc_veto(NOTES)
    _, h1 = h_cons(after)
    print(f"\nAprès veto P2 sur voile (quasi-consensus) : H_cons {h0:.3f} -> {h1:.3f}  (Δ={h1-h0:+.3f})")
    print("Le progrès n'est pas monotone : un grief nouveau remonte H.")
    print("\nMétriques :")
    print(f"  H_cons: {h0:.3f}")
    print(f"  H_max_dim: {max(h_dim, key=h_dim.get)}={max(h_dim.values()):.3f}")
    print(f"  question_max_gain: {dim}")
    print(f"  desaccord_moyen: {mat.values.sum() / (len(mat) ** 2 - len(mat)):.3f}")
    print(f"  delta_choc_veto: {h1 - h0:.3f}")


if __name__ == "__main__":
    main()
