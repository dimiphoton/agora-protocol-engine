"""Ontologie unique partagée + mapping des désaccords vers des concepts communs.

Scénario jouet : 3 participants choisissent des vacances (échange 4).
Les énoncés sont en langage libre ; le graphe commun infère les contraintes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Iterable

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Ontologie (graphe de connaissances minimal, pas de RDF)
# ---------------------------------------------------------------------------

IS_A: dict[str, str] = {
    "voile": "activite_nautique",
    "surf": "activite_nautique",
    "velotourisme": "activite_terrestre",
    "randonnee": "activite_terrestre",
    "festivals": "activite_festive",
    "camping": "hebergement_nature",
    "hotel": "hebergement_confort",
    "gite": "hebergement_confort",
    "bretagne": "destination",
    "mediterranee": "destination",
    "auvergne": "destination",
}

REQUIERT: dict[str, str] = {
    "activite_nautique": "acces_mer",
    "voile": "acces_mer",
}

A_POUR: dict[str, set[str]] = {
    "bretagne": {"acces_mer", "climat_tempere", "relief_valonne"},
    "mediterranee": {"acces_mer", "climat_chaud", "ambiance_festive_possible"},
    "auvergne": {"relief_valonne", "nature", "climat_tempere"},
}

IMPLIQUE: dict[str, set[str]] = {
    "festivals": {"ambiance_festive", "budget_eleve", "bruit"},
    "camping": {"nature", "budget_faible", "inconfort_possible"},
    "hotel": {"confort", "budget_moyen"},
    "velotourisme": {"effort_physique", "nature"},
}

INCOMPATIBLE: dict[str, set[str]] = {
    "festivals": {"calme"},
    "camping": {"luxe"},
    "auvergne": {"acces_mer"},
    "velotourisme": {"plat_pays"},
}

# Lexique : mots des humains -> concept commun.
LEXIQUE: dict[str, str] = {
    "voile": "voile",
    "bateau": "voile",
    "nautisme": "voile",
    "surf": "surf",
    "velo": "velotourisme",
    "velotourisme": "velotourisme",
    "randonnee": "randonnee",
    "marche": "randonnee",
    "festival": "festivals",
    "festivals": "festivals",
    "teuf": "festivals",
    "camping": "camping",
    "tente": "camping",
    "hotel": "hotel",
    "palace": "hotel",
    "gite": "gite",
    "bretagne": "bretagne",
    "bzh": "bretagne",
    "mediterranee": "mediterranee",
    "med": "mediterranee",
    "sud": "mediterranee",
    "auvergne": "auvergne",
    "mer": "acces_mer",
    "plage": "acces_mer",
    "calme": "calme",
    "luxe": "luxe",
    "confort": "confort",
    "nature": "nature",
    "bruit": "bruit",
    "budget": "budget_faible",
}


@dataclass
class Enonce:
    participant: str
    texte: str
    polarite: int  # +1 aime, -1 refuse, 0 neutre
    intensite: float = 1.0


@dataclass
class Mapping:
    enonce: Enonce
    concept: str | None
    orphelin: bool


@dataclass
class Resultat:
    mappings: list[Mapping]
    inferences: list[str]
    conflits: list[tuple[str, str, str]]
    options: pd.DataFrame
    metriques: dict[str, float] = field(default_factory=dict)


def normalise(mot: str) -> str:
    return mot.lower().strip(" .,!?;:\"'")


def mapper(enonces: Iterable[Enonce]) -> list[Mapping]:
    out: list[Mapping] = []
    for e in enonces:
        trouves: list[str] = []
        for token in e.texte.replace("-", " ").replace("'", " ").split():
            cle = normalise(token)
            if cle in LEXIQUE and LEXIQUE[cle] not in trouves:
                trouves.append(LEXIQUE[cle])
        if not trouves:
            out.append(Mapping(enonce=e, concept=None, orphelin=True))
        else:
            for c in trouves:
                out.append(Mapping(enonce=e, concept=c, orphelin=False))
    return out


def fermeture(concept: str) -> set[str]:
    """Ancêtres + implications + attributs de destination."""
    vus: set[str] = {concept}
    pile = [concept]
    while pile:
        c = pile.pop()
        parent = IS_A.get(c)
        if parent and parent not in vus:
            vus.add(parent)
            pile.append(parent)
        for impl in IMPLIQUE.get(c, set()):
            if impl not in vus:
                vus.add(impl)
                pile.append(impl)
        for attr in A_POUR.get(c, set()):
            if attr not in vus:
                vus.add(attr)
                pile.append(attr)
        req = REQUIERT.get(c)
        if req and req not in vus:
            vus.add(req)
            pile.append(req)
    return vus


def inferer(concepts_actifs: set[str]) -> list[str]:
    notes: list[str] = []
    for c in concepts_actifs:
        for impl in IMPLIQUE.get(c, set()):
            notes.append(f"{c} implique {impl}")
        f = fermeture(c)
        for dest in concepts_actifs & {"bretagne", "mediterranee", "auvergne"}:
            for x in f:
                req = REQUIERT.get(x)
                if req and req not in A_POUR.get(dest, set()):
                    notes.append(f"{c} requiert {req} mais {dest} ne l'a pas")
    opts = enumerer_options()
    for _, row in opts[~opts["valide"]].iterrows():
        notes.append(
            f"option ({row.destination}, {row.logement}, {row.activite}) "
            f"éliminée : {row.raison}"
        )
    return sorted(set(notes))


def conflits_sur_meme_concept(mappings: list[Mapping]) -> list[tuple[str, str, str]]:
    par_concept: dict[str, list[Mapping]] = {}
    for m in mappings:
        if m.concept is None:
            continue
        par_concept.setdefault(m.concept, []).append(m)
    conflits: list[tuple[str, str, str]] = []
    for concept, ms in par_concept.items():
        aiment = [m.enonce.participant for m in ms if m.enonce.polarite > 0]
        refusent = [m.enonce.participant for m in ms if m.enonce.polarite < 0]
        for a in aiment:
            for r in refusent:
                conflits.append((concept, a, r))
    return conflits


def option_valide(dest: str, logement: str, activite: str) -> tuple[bool, str]:
    concepts = {dest, logement, activite}
    fermes = set()
    for c in concepts:
        fermes |= fermeture(c)
    for c in list(fermes):
        req = REQUIERT.get(c)
        if req and req not in A_POUR.get(dest, set()) and req not in fermes:
            return False, f"{c} requiert {req}"
        for interdit in INCOMPATIBLE.get(c, set()):
            if interdit in fermes or interdit in A_POUR.get(dest, set()):
                return False, f"{c} incompatible avec {interdit}"
        # destination sans l'attribut requis
        if c in REQUIERT:
            besoin = REQUIERT[c]
            if besoin not in A_POUR.get(dest, set()):
                return False, f"{dest} n'offre pas {besoin}"
    if "activite_nautique" in fermes and "acces_mer" not in A_POUR.get(dest, set()):
        return False, f"{activite} requiert acces_mer, absent de {dest}"
    return True, "ok"


def enumerer_options() -> pd.DataFrame:
    dests = ["bretagne", "mediterranee", "auvergne"]
    logements = ["camping", "hotel", "gite"]
    activites = ["voile", "velotourisme", "festivals", "randonnee"]
    rows = []
    for d, l, a in product(dests, logements, activites):
        ok, raison = option_valide(d, l, a)
        rows.append({"destination": d, "logement": l, "activite": a, "valide": ok, "raison": raison})
    return pd.DataFrame(rows)


def scenario_vacances() -> list[Enonce]:
    """Énoncés bruts, volontairement hétérogènes, à mapper."""
    return [
        Enonce("P1", "je veux du velo et la bretagne", +1, 1.0),
        Enonce("P1", "pas d'hotel palace", -1, 0.8),
        Enonce("P1", "tente ok", +1, 0.6),
        Enonce("P2", "med et festivals", +1, 1.0),
        Enonce("P2", "camping c'est non", -1, 1.0),
        Enonce("P2", "besoin de confort", +1, 0.9),
        Enonce("P3", "voile sur la mer", +1, 1.0),
        Enonce("P3", "pas trop de teuf", -1, 0.7),
        Enonce("P3", "gite ca me va", +1, 0.5),
        Enonce("P2", "le glamping c'est autre chose", +1, 0.4),  # orphelin volontaire
        Enonce("P1", "j'aime le bzh", +1, 0.5),
    ]


def evaluer(enonces: list[Enonce] | None = None) -> Resultat:
    enonces = enonces or scenario_vacances()
    mappings = mapper(enonces)
    concepts = {m.concept for m in mappings if m.concept}
    inferences = inferer(concepts)
    conflits = conflits_sur_meme_concept(mappings)
    options = enumerer_options()
    n = len(mappings)
    n_orphelin = sum(1 for m in mappings if m.orphelin)
    n_valides = int(options["valide"].sum())
    metriques = {
        "n_enonces": float(n),
        "taux_mapping": 1.0 - n_orphelin / n,
        "n_orphelins": float(n_orphelin),
        "n_concepts_actifs": float(len(concepts)),
        "n_inferences": float(len(inferences)),
        "n_conflits_conceptuels": float(len(conflits)),
        "n_options_totales": float(len(options)),
        "n_options_valides": float(n_valides),
        "taux_filtrage": 1.0 - n_valides / len(options),
    }
    return Resultat(mappings, inferences, conflits, options, metriques)


def afficher(res: Resultat) -> None:
    print("=== Ontologie unique — scénario vacances ===")
    print("\nMappings :")
    for m in res.mappings:
        pol = {1: "+", -1: "-", 0: "0"}[int(np.sign(m.enonce.polarite) or 0)]
        cible = m.concept or "ORPHELIN"
        print(f"  {m.enonce.participant} {pol} «{m.enonce.texte}» -> {cible}")
    print("\nInférences :")
    for inf in res.inferences:
        print(f"  - {inf}")
    print("\nConflits sur un même concept :")
    for c, a, r in res.conflits:
        print(f"  - {c}: {a} pour vs {r} contre")
    print("\nFiltrage des options :")
    print(res.options.groupby("valide").size().to_string())
    print("\nExemples invalidés (Auvergne+voile attendu) :")
    mauvais = res.options[(res.options.destination == "auvergne") & (res.options.activite == "voile")]
    print(mauvais.to_string(index=False))
    print("\nMétriques :")
    for k, v in res.metriques.items():
        print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")


def main() -> None:
    afficher(evaluer())


if __name__ == "__main__":
    main()
