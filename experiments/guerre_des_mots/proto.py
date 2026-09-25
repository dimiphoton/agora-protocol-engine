"""Confrontation d'ontologies privées : alignement, traduction, divergence.

Chaque parti a son vocabulaire. On mesure la guerre des mots, on propose
des termes-ponts (neutralisation), on sépare le désaccord lexical du
désaccord réel.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Ontologies privées : label local -> polarité sur un référent interne
# Le référent est un id neutre que le maître d'expérience connaît ; les
# participants, eux, n'emploient que leurs labels.

ONTO_P1 = {
    "aventure": +1,
    "liberte_sous_tente": +1,      # camping
    "cage_a_touristes": -1,        # hotel
    "bzh": +1,                     # bretagne
    "usine_a_bronzette": -1,       # mediterranee
    "roue_libre": +1,              # velotourisme
    "foire_commerciale": -1,       # festivals
}

ONTO_P2 = {
    "confort_civilise": +1,        # hotel
    "precarite_hygienique": -1,    # camping
    "sud_qui_vit": +1,             # mediterranee
    "finistere_humide": -1,        # bretagne
    "nuit_electrique": +1,         # festivals
    "penitence_cycliste": -1,      # velotourisme
}

ONTO_P3 = {
    "planche_et_vent": +1,         # voile
    "mer_ouverte": +1,             # acces_mer / med ou bretagne
    "tapage_nocturne": -1,         # festivals
    "nid_doux": +1,                # gite
    "grande_surface_hoteliere": -1,  # hotel de masse
}

# Table d'alignement : label privé -> concept-pont (ontologie de négociation)
ALIGNEMENT: dict[str, str] = {
    "aventure": "activite_terrestre",
    "liberte_sous_tente": "camping",
    "cage_a_touristes": "hotel",
    "bzh": "bretagne",
    "usine_a_bronzette": "mediterranee",
    "roue_libre": "velotourisme",
    "foire_commerciale": "festivals",
    "confort_civilise": "hotel",
    "precarite_hygienique": "camping",
    "sud_qui_vit": "mediterranee",
    "finistere_humide": "bretagne",
    "nuit_electrique": "festivals",
    "penitence_cycliste": "velotourisme",
    "planche_et_vent": "voile",
    "mer_ouverte": "acces_mer",
    "tapage_nocturne": "festivals",
    "nid_doux": "gite",
    "grande_surface_hoteliere": "hotel",
}

# Termes-ponts proposés par le « lexicographe » quand deux labels
# opposés visent le même concept.
PONTS: dict[str, str] = {
    "camping": "hebergement_leger",
    "hotel": "hebergement_servi",
    "bretagne": "faconade_atlantique",
    "mediterranee": "faconade_sud",
    "festivals": "evenement_collectif",
    "velotourisme": "mobilite_humaine",
    "voile": "deplacement_nautique",
    "gite": "hebergement_autonomome",
}


@dataclass
class Parti:
    nom: str
    onto: dict[str, int]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def divergence_lexicale(partis: list[Parti]) -> float:
    labels = [set(p.onto) for p in partis]
    scores = []
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            scores.append(1.0 - jaccard(a, b))
    return float(np.mean(scores)) if scores else 0.0


def projeter(parti: Parti) -> dict[str, int]:
    """Traduit l'ontologie privée vers les concepts-ponts."""
    proj: dict[str, int] = {}
    for label, pol in parti.onto.items():
        concept = ALIGNEMENT.get(label)
        if concept is None:
            continue
        # si deux labels du même parti tombent sur le même concept, on moyenne
        proj[concept] = int(np.sign(proj.get(concept, 0) + pol) or pol)
    return proj


def divergence_alignee(partis: list[Parti]) -> float:
    projections = [set(projeter(p)) for p in partis]
    scores = []
    for i, a in enumerate(projections):
        for b in projections[i + 1 :]:
            scores.append(1.0 - jaccard(a, b))
    return float(np.mean(scores)) if scores else 0.0


def guerres_residuelles(partis: list[Parti]) -> pd.DataFrame:
    """Même concept, polarités opposées : vrai conflit, plus lexical."""
    rows = []
    projs = [(p.nom, projeter(p)) for p in partis]
    concepts = sorted({c for _, d in projs for c in d})
    for c in concepts:
        polarites = {nom: d[c] for nom, d in projs if c in d}
        if len(polarites) < 2:
            continue
        vals = list(polarites.values())
        if min(vals) < 0 < max(vals):
            pour = [n for n, v in polarites.items() if v > 0]
            contre = [n for n, v in polarites.items() if v < 0]
            pont = PONTS.get(c)
            rows.append({
                "concept": c,
                "pour": ",".join(pour),
                "contre": ",".join(contre),
                "pont": pont or "",
                "neutralisable": pont is not None,
            })
    return pd.DataFrame(rows)


def evaluer() -> dict[str, float]:
    partis = [
        Parti("P1_aventurier", ONTO_P1),
        Parti("P2_fete", ONTO_P2),
        Parti("P3_sportif", ONTO_P3),
    ]
    d_lex = divergence_lexicale(partis)
    d_ali = divergence_alignee(partis)
    guerres = guerres_residuelles(partis)
    n_w = len(guerres)
    n_neutre = int(guerres["neutralisable"].sum()) if n_w else 0
    recouvrement = []
    for p in partis:
        recouvrement.append(sum(1 for k in p.onto if k in ALIGNEMENT) / len(p.onto))
    return {
        "divergence_lexicale": d_lex,
        "divergence_alignee": d_ali,
        "delta_divergence": d_lex - d_ali,
        "n_guerres_residuelles": float(n_w),
        "taux_neutralisation": n_neutre / n_w if n_w else 1.0,
        "residual_wars": float(n_w - n_neutre),
        "taux_alignement_labels": float(np.mean(recouvrement)),
        "n_labels_prives": float(sum(len(p.onto) for p in partis)),
        "n_concepts_ponts": float(len(set(ALIGNEMENT.values()))),
    }, partis, guerres


def afficher() -> None:
    metriques, partis, guerres = evaluer()
    print("=== Guerre des mots — ontologies privées (vacances) ===")
    for p in partis:
        print(f"\n{p.nom} ({len(p.onto)} labels) :")
        for label, pol in p.onto.items():
            cible = ALIGNEMENT.get(label, "?")
            signe = "+" if pol > 0 else "-"
            print(f"  {signe} {label:28s} -> {cible}")
    print("\nGuerres résiduelles (même concept, polarités opposées) :")
    if guerres.empty:
        print("  (aucune)")
    else:
        print(guerres.to_string(index=False))
    print("\nMétriques :")
    for k, v in metriques.items():
        print(f"  {k}: {v:.3f}")
    print(
        "\nLecture : si delta_divergence >> 0, une grande part du conflit "
        "était une guerre de vocabulaire. residual_wars=0 ici car tous les "
        "concepts ont un pont ; le pont NE supprime pas le désaccord de "
        "préférence, il le rend dicible dans une langue commune."
    )


def main() -> None:
    afficher()


if __name__ == "__main__":
    main()
