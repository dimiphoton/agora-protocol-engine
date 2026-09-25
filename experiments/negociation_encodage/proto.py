"""DSL / config pour encoder une négociation : veto, rounds, anonymat, rétribution.

Jouable en script. Deux scénarios YAML : vacances (amis) et copropriété
(inconnus). Aucune blockchain : la config est un artefact off-chain.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

SCENES = {
    "vacances_amis": {
        "options": ["bretagne_gite_voile", "med_hotel_festivals", "bretagne_hotel_voile", "auv_gite_rando"],
        "notes": {
            "P1": [6, -4, 3, 2],
            "P2": [-3, 8, 4, -5],
            "P3": [5, -2, 7, 1],
        },
        "veto_sur": {"P2": "bretagne_hotel_voile", "P3": "med_hotel_festivals"},
    },
    "copropriete_toiture": {
        "options": ["tuiles_pro", "zinc_cher", "patch_pas_cher", "attente_hiver"],
        "notes": {
            "A_rdc": [4, -2, 5, -6],
            "B_etage": [3, 6, -3, -8],
            "C_combles": [2, 8, -7, -9],
        },
        "veto_sur": {"C_combles": "tuiles_pro", "A_rdc": "zinc_cher"},
    },
}


@dataclass
class Proto:
    nom: str
    rounds: int
    anonymat: bool
    fitness: str
    entropie_seuil: float
    veto_mode: str
    veto_prix: int
    penalite_score: float
    retrib_vote: int
    retrib_concession: int
    bonus_delta_h: int
    budget: dict[str, int]


def charger(path: Path) -> Proto:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["protocol"]
    v, r, b = raw["veto"], raw["retrib"], raw["budget_tokens"]
    return Proto(
        nom=raw["nom"],
        rounds=int(raw["rounds"]),
        anonymat=bool(raw["anonymat"]),
        fitness=str(raw["fitness"]),
        entropie_seuil=float(raw["entropie_seuil"]),
        veto_mode=str(v["mode"]),
        veto_prix=int(v["prix"]),
        penalite_score=float(v["penalite_score"]),
        retrib_vote=int(r["vote"]),
        retrib_concession=int(r["concession"]),
        bonus_delta_h=int(r["bonus_delta_h"]),
        budget={k: int(x) for k, x in b.items()},
    )


def shannon_signes(vals: list[float]) -> float:
    urnes = [sum(1 for x in vals if x < 0), sum(1 for x in vals if x == 0), sum(1 for x in vals if x > 0)]
    total = sum(urnes)
    p = np.array([u / total for u in urnes if u])
    return (float(-np.sum(p * np.log2(p))) + 0.0) if p.size else 0.0


def agregat(scores: list[float], mode: str) -> float:
    if mode == "moyenne":
        return float(np.mean(scores))
    if mode == "enthousiasme":
        return float(np.max(scores))
    return float(np.min(scores))  # least_misery


def nom_public(pid: str, proto: Proto, alias: dict[str, str]) -> str:
    return alias[pid] if proto.anonymat else pid


def jouer(proto: Proto, rng: np.random.Generator | None = None) -> dict:
    rng = rng or np.random.default_rng(0)
    scene = SCENES[proto.nom]
    options: list[str] = list(scene["options"])
    notes = {p: np.array(v, dtype=float) for p, v in scene["notes"].items()}
    veto_sur: dict[str, str] = dict(scene["veto_sur"])
    people = list(notes)
    alias = {p: f"agent_{i+1}" for i, p in enumerate(people)}
    tokens = dict(proto.budget)
    retrib = {p: 0 for p in people}
    veto_payes = 0
    cout_veto = 0
    concessions = 0
    journal: list[str] = []
    h_hist: list[float] = []
    best_opt, best_score = options[0], -1e9

    # option courante : celle au least misery initial, hors veto payé
    paid: set[str] = set()

    def evaluer() -> tuple[str, float, dict[str, float], float]:
        ranking = []
        for i, opt in enumerate(options):
            sc = {}
            for p in people:
                s = float(notes[p][i])
                if veto_sur.get(p) == opt and p in paid:
                    if proto.veto_mode == "dur":
                        s = -1e6
                    else:
                        s -= proto.penalite_score
                sc[p] = s
            ranking.append((agregat(list(sc.values()), proto.fitness), opt, sc))
        ranking.sort(reverse=True)
        fit, opt, sc = ranking[0]
        h = shannon_signes(list(sc.values()))
        return opt, fit, sc, h

    for r in range(1, proto.rounds + 1):
        opt, fit, sc, h = evaluer()
        h_hist.append(h)
        for p in people:
            tokens[p] += proto.retrib_vote
            retrib[p] += proto.retrib_vote
        for p, cible in list(veto_sur.items()):
            if cible == opt and p not in paid and tokens[p] >= proto.veto_prix:
                tokens[p] -= proto.veto_prix
                cout_veto += proto.veto_prix
                veto_payes += 1
                paid.add(p)
                journal.append(
                    f"R{r} VETO {nom_public(p, proto, alias)} paie {proto.veto_prix} "
                    f"contre {opt}"
                )
        if r >= 2 and abs(h_hist[-1] - h_hist[-2]) < 0.05:
            for p, cible in list(veto_sur.items()):
                if p in paid and rng.random() < 0.55:
                    veto_sur.pop(p, None)
                    paid.discard(p)
                    tokens[p] += proto.retrib_concession
                    retrib[p] += proto.retrib_concession
                    concessions += 1
                    journal.append(
                        f"R{r} CONCESSION {nom_public(p, proto, alias)} lève le veto "
                        f"({'+'+str(proto.retrib_concession)} tok)"
                    )
                    break
        opt, fit, sc, h = evaluer()
        if len(h_hist) >= 2 and h_hist[-2] - h > 0.15:
            for p in people:
                tokens[p] += proto.bonus_delta_h
                retrib[p] += proto.bonus_delta_h
            journal.append(f"R{r} BONUS ΔH={h_hist[-2]-h:.2f}")
        h_hist[-1] = h
        journal.append(
            f"R{r} option={opt} fitness={fit:.1f} H={h:.3f} "
            f"scores={ {nom_public(p, proto, alias): round(s,1) for p,s in sc.items()} }"
        )
        if fit > best_score:
            best_opt, best_score = opt, fit
        if h <= proto.entropie_seuil and r > 1 and veto_payes == 0:
            journal.append(f"STOP palier H≤{proto.entropie_seuil}")
            break
        if h <= proto.entropie_seuil and r > 1 and concessions:
            journal.append(f"STOP palier H≤{proto.entropie_seuil} après concession")
            break

    return {
        "scenario": proto.nom,
        "anonymat": proto.anonymat,
        "fitness": proto.fitness,
        "rounds_max": proto.rounds,
        "rounds_joues": len([j for j in journal if j.startswith("R") and "option=" in j]),
        "vetos_declenches": veto_payes,
        "cout_veto_total": cout_veto,
        "concessions": concessions,
        "retributions_total": int(sum(retrib.values())),
        "least_misery_final": best_score if proto.fitness == "least_misery" else float(np.min(list(sc.values()))),
        "option_finale": best_opt,
        "H_final": h_hist[-1] if h_hist else float("nan"),
        "H_initial": h_hist[0] if h_hist else float("nan"),
        "tokens_restants": tokens,
        "journal": journal,
    }


def main() -> None:
    here = Path(__file__).parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(here / "vacances.yaml"))
    args = parser.parse_args()
    proto = charger(Path(args.config))
    res = jouer(proto)
    print(f"=== Négociation encodée : {proto.nom} ===")
    print(f"anonymat={proto.anonymat}  fitness={proto.fitness}  "
          f"veto={proto.veto_mode}/{proto.veto_prix}tok  rounds≤{proto.rounds}")
    print("\nJournal :")
    for line in res["journal"]:
        print(" ", line)
    print("\nMétriques :")
    for k, v in res.items():
        if k == "journal":
            continue
        print(f"  {k}: {v}")
    print(
        "\nLecture : changer le YAML change le jeu (pas le moteur). "
        "Copropriété = anonymat + veto cher + plus de rounds, parce que "
        "les gens ne se font pas confiance. Vacances = veto bon marché."
    )


if __name__ == "__main__":
    main()
