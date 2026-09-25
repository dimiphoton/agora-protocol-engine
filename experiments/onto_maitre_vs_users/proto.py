"""Comparer : le maître définit les branches vs les utilisateurs étendent.

Mesure cohérence (contradictions, cycles, orphelins) vs expressivité
(couverture des énoncés) et risque de capture.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

Relation = tuple[str, str, str]  # (src, type, dst)  type in {is_a, requiert, incompatible, implique}


MASTER_NODES = {
    "destination", "bretagne", "mediterranee", "auvergne",
    "logement", "camping", "hotel", "gite",
    "activite", "voile", "velotourisme", "festivals", "randonnee",
    "acces_mer", "confort", "nature", "bruit", "calme", "budget_eleve",
}

MASTER_RELATIONS: list[Relation] = [
    ("bretagne", "is_a", "destination"),
    ("mediterranee", "is_a", "destination"),
    ("auvergne", "is_a", "destination"),
    ("camping", "is_a", "logement"),
    ("hotel", "is_a", "logement"),
    ("gite", "is_a", "logement"),
    ("voile", "is_a", "activite"),
    ("velotourisme", "is_a", "activite"),
    ("festivals", "is_a", "activite"),
    ("randonnee", "is_a", "activite"),
    ("voile", "requiert", "acces_mer"),
    ("bretagne", "implique", "acces_mer"),
    ("mediterranee", "implique", "acces_mer"),
    ("auvergne", "incompatible", "acces_mer"),
    ("festivals", "implique", "bruit"),
    ("festivals", "incompatible", "calme"),
    ("camping", "implique", "nature"),
    ("hotel", "implique", "confort"),
]


@dataclass
class Edit:
    auteur: str
    src: str
    type_rel: str
    dst: str
    confiance: float = 0.5  # 0..1, vote d'éditeur


# Les utilisateurs veulent parler de choses hors arbre maître.
USER_EDITS: list[Edit] = [
    Edit("P1", "glamping", "is_a", "camping", 0.4),
    Edit("P1", "glamping", "implique", "confort", 0.6),  # tension avec camping rustique
    Edit("P1", "bikepacking", "is_a", "velotourisme", 0.9),
    Edit("P2", "glamping", "is_a", "hotel", 0.3),  # CONTRADICTION is_a double parent discordant
    Edit("P2", "after_party", "is_a", "festivals", 0.8),
    Edit("P2", "after_party", "implique", "bruit", 0.9),
    Edit("P2", "all_inclusive", "is_a", "hotel", 0.7),
    Edit("P3", "ecole_de_voile", "is_a", "voile", 0.8),
    Edit("P3", "ecole_de_voile", "requiert", "acces_mer", 0.95),
    Edit("P3", "silence_nuit", "is_a", "calme", 0.7),
    Edit("P1", "camping", "incompatible", "confort", 0.5),  # contredit glamping->confort
    Edit("P2", "mediterranee", "implique", "budget_eleve", 0.6),
    # cycle volontaire
    Edit("P2", "bruit", "implique", "festivals", 0.2),
    # orphelin : nœud sans rattachement à la racine métier
    Edit("P1", "karma_vacances", "implique", "bonne_vibes", 0.1),
]


ENONCES_COUVERTURE = [
    "glamping", "bikepacking", "after_party", "all_inclusive",
    "ecole_de_voile", "silence_nuit", "voile", "camping", "hotel",
    "karma_vacances", "spa",  # spa jamais ajouté
]


def has_cycle(relations: list[Relation]) -> bool:
    graph: dict[str, list[str]] = defaultdict(list)
    for src, typ, dst in relations:
        if typ in {"is_a", "implique", "requiert"}:
            graph[src].append(dst)
    visiting: set[str] = set()
    seen: set[str] = set()

    def dfs(n: str) -> bool:
        if n in visiting:
            return True
        if n in seen:
            return False
        visiting.add(n)
        for nxt in graph[n]:
            if dfs(nxt):
                return True
        visiting.remove(n)
        seen.add(n)
        return False

    return any(dfs(n) for n in list(graph))


def contradictions(relations: list[Relation]) -> list[str]:
    """incompatible(a,b) alors qu'un chemin implique/is_a relie a et b, ou double is_a discordant."""
    impl: dict[str, set[str]] = defaultdict(set)
    isa: dict[str, set[str]] = defaultdict(set)
    incom: list[tuple[str, str]] = []
    for src, typ, dst in relations:
        if typ in {"implique", "requiert", "is_a"}:
            impl[src].add(dst)
        if typ == "is_a":
            isa[src].add(dst)
        if typ == "incompatible":
            incom.append((src, dst))

    def fermer(start: str) -> set[str]:
        vus = {start}
        pile = [start]
        while pile:
            c = pile.pop()
            for n in impl[c]:
                if n not in vus:
                    vus.add(n)
                    pile.append(n)
        return vus

    notes: list[str] = []
    for src, dst in incom:
        if dst in fermer(src) or src in fermer(dst):
            notes.append(f"incompatible({src},{dst}) contredit une implication")
    for src, parents in isa.items():
        if len(parents) > 1:
            notes.append(f"{src} a plusieurs is_a {sorted(parents)}")
    return notes


def orphelins(nodes: set[str], relations: list[Relation], racines: set[str]) -> set[str]:
    touches = set()
    for src, _, dst in relations:
        touches.add(src)
        touches.add(dst)
    rattaches = set(racines)
    changed = True
    while changed:
        changed = False
        for src, typ, dst in relations:
            if typ == "is_a" and dst in rattaches and src not in rattaches:
                rattaches.add(src)
                changed = True
            if typ in {"implique", "requiert"} and src in rattaches and dst not in rattaches:
                rattaches.add(dst)
                changed = True
    return (nodes | touches) - rattaches


@dataclass
class Regime:
    nom: str
    nodes: set[str]
    relations: list[Relation]
    edits: list[Edit] = field(default_factory=list)

    def metriques(self, racines: set[str], enonces: list[str]) -> dict[str, float]:
        contras = contradictions(self.relations)
        cycle = has_cycle(self.relations)
        orph = orphelins(self.nodes, self.relations, racines)
        n_rel = max(len(self.relations), 1)
        penalites = len(contras) + int(cycle) + len(orph)
        coherence = max(0.0, 1.0 - penalites / n_rel)
        representables = sum(1 for e in enonces if e in self.nodes)
        expressivite = representables / len(enonces)
        if self.edits:
            par_auteur: dict[str, int] = defaultdict(int)
            for ed in self.edits:
                par_auteur[ed.auteur] += 1
            capture = max(par_auteur.values()) / len(self.edits)
            confiance = float(np.mean([ed.confiance for ed in self.edits]))
        else:
            capture = 0.0
            confiance = 1.0
        return {
            "n_noeuds": float(len(self.nodes)),
            "n_relations": float(len(self.relations)),
            "n_contradictions": float(len(contras)),
            "a_cycle": float(cycle),
            "n_orphelins": float(len(orph)),
            "coherence": coherence,
            "expressivite": expressivite,
            "capture": capture,
            "confiance_moyenne": confiance,
            "produit_coh_expr": coherence * expressivite,
        }


def regime_maitre() -> Regime:
    return Regime("maitre", set(MASTER_NODES), list(MASTER_RELATIONS), [])


def regime_users() -> Regime:
    nodes = set(MASTER_NODES)
    rels = list(MASTER_RELATIONS)
    for ed in USER_EDITS:
        nodes.add(ed.src)
        nodes.add(ed.dst)
        rels.append((ed.src, ed.type_rel, ed.dst))
    return Regime("users", nodes, rels, list(USER_EDITS))


def main() -> None:
    racines = {"destination", "logement", "activite"}
    m = regime_maitre()
    u = regime_users()
    mm = m.metriques(racines, ENONCES_COUVERTURE)
    uu = u.metriques(racines, ENONCES_COUVERTURE)
    df = pd.DataFrame([{"regime": "maitre", **mm}, {"regime": "users", **uu}])
    print("=== Maître vs utilisateurs — extension de l'ontologie ===")
    print(df.round(3).to_string(index=False))
    print("\nContradictions côté users :")
    for c in contradictions(u.relations):
        print(f"  - {c}")
    print(f"\nCycle users : {has_cycle(u.relations)}")
    print(f"Orphelins users : {sorted(orphelins(u.nodes, u.relations, racines))}")
    print(
        "\nLecture : le maître gagne en cohérence, perd en expressivité "
        "(glamping, spa, karma absents). Les users inversent. Le produit "
        "cohérence×expressivité est le score d'utilité hybride. Une règle "
        "simple : le maître pose le tronc ; les users n'ajoutent une branche "
        "que si confiance ≥ 0.6 et pas de contradiction."
    )
    # filtrage par confiance
    rels_filtrees = list(MASTER_RELATIONS)
    nodes_f = set(MASTER_NODES)
    gardes = []
    for ed in USER_EDITS:
        if ed.confiance >= 0.6:
            gardes.append(ed)
            nodes_f.add(ed.src)
            nodes_f.add(ed.dst)
            rels_filtrees.append((ed.src, ed.type_rel, ed.dst))
    hyb = Regime("hybride_confiance>=0.6", nodes_f, rels_filtrees, gardes)
    hh = hyb.metriques(racines, ENONCES_COUVERTURE)
    print("\nHybride (confiance ≥ 0.6) :")
    for k, v in hh.items():
        print(f"  {k}: {v:.3f}")


if __name__ == "__main__":
    main()
