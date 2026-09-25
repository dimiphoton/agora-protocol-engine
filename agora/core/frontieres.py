"""Géométrie de l'espace de négociation, avant l'algorithme génétique.

Deux ensembles distincts :

- le **domaine valide** : combinaisons qui passent ``requiert`` et
  ``incompatible``. C'est le terrain où le génétique a le droit de muter ;
- la **région acceptable** : parmi ces combinaisons, celles dont le
  least misery est au moins égal à un seuil. Le veto ne retire rien :
  il creuse une falaise de coût.

La frontière acceptable est le bord discret de cette région : un point
acceptable dont un voisin (un seul gène différent) est valide mais
sous le seuil.
"""

from __future__ import annotations

import networkx as nx

from agora.core.evaluation import classer
from agora.core.scores import VETO_COUT
from agora.kr.charger import charger
from agora.kr.requetes import (
    combinaison_valide,
    dimensions,
    enumerer_candidats,
    etendre_preferences,
    identifiant_candidat,
    participants,
    valeurs,
)

# Au-delà, on ne construit pas tout le produit : la carte serait un mensonge
# si on n'en montrait qu'un coin sans le dire.
PLAFOND_PAYSAGE = 8000
SEUIL_ACCEPTABLE = 0.0


def analyser_frontieres(
    scenario: dict,
    preferences: dict,
    seuil: float = SEUIL_ACCEPTABLE,
) -> dict:
    """Décrit l'espace, la falaise de veto, le Pareto et une coupe 2D.

    ``seuil`` est le least misery minimum pour qu'un candidat soit
    acceptable. Défaut : 0 (personne en dessous de la note neutre,
    une fois le veto soustrait).
    """
    graphe = charger(scenario)
    produit = taille_produit(graphe)
    dims = dimensions(graphe)
    if produit > PLAFOND_PAYSAGE:
        return {
            "complet": False,
            "seuil": float(seuil),
            "espace": _espace(graphe, produit, None),
            "message": (
                f"Produit cartésien {produit} au-dessus de {PLAFOND_PAYSAGE}. "
                "Le paysage complet n'est pas construit : c'est le cas "
                "où l'algorithme génétique remplace l'énumération."
            ),
        }

    etendues = etendre_preferences(graphe, preferences)
    ids = [personne["id"] for personne in participants(graphe)]
    evalues = classer(
        enumerer_candidats(graphe),
        ids,
        etendues["notes"],
        etendues["veto"],
        graphe,
    )
    return _depuis_evalues(graphe, evalues, float(seuil))


def taille_produit(graphe: nx.MultiDiGraph) -> int:
    """Nombre de génomes avant les contraintes du graphe."""
    total = 1
    dims = dimensions(graphe)
    if not dims:
        return 0
    for dimension in dims:
        total *= len(valeurs(graphe, dimension))
    return total


def _depuis_evalues(
    graphe: nx.MultiDiGraph,
    evalues: list[dict],
    seuil: float,
) -> dict:
    par_id = {candidat["id"]: candidat for candidat in evalues}
    pareto_ids = _ids_pareto(evalues)
    acceptables = [
        candidat
        for candidat in evalues
        if float(candidat["least_misery"]) >= seuil
    ]
    falaise = [
        candidat
        for candidat in evalues
        if float(candidat["penalite"]) > 0
    ]
    frontiere = []
    frontiere_dure = []
    for candidat in evalues:
        voisins = _voisins_valides(graphe, candidat, par_id)
        hors = [
            voisin["id"]
            for voisin in voisins
            if float(voisin["least_misery"]) < seuil
        ]
        if float(candidat["least_misery"]) >= seuil and hors:
            frontiere.append(
                {
                    "id": candidat["id"],
                    "least_misery": candidat["least_misery"],
                    "voisins_sous_seuil": hors,
                }
            )
        if _a_un_voisin_invalide(graphe, candidat["choix"]):
            frontiere_dure.append(candidat["id"])

    return {
        "complet": True,
        "seuil": seuil,
        "cout_veto": VETO_COUT,
        "espace": _espace(graphe, taille_produit(graphe), len(evalues)),
        "acceptable": {
            "n": len(acceptables),
            "taux_parmi_valides": _taux(len(acceptables), len(evalues)),
            "definition": "least_misery >= seuil",
        },
        "falaise_veto": {
            "n": len(falaise),
            "saut": VETO_COUT,
            "ids": [candidat["id"] for candidat in falaise],
        },
        "pareto": sorted(pareto_ids),
        "frontiere_acceptable": frontiere,
        "frontiere_dure": frontiere_dure,
        "marginales": _marginales(graphe, evalues, seuil),
        "coupe": _coupe(graphe, evalues, seuil),
        "points": [_point(candidat, seuil, pareto_ids, frontiere) for candidat in evalues],
    }


def _espace(graphe: nx.MultiDiGraph, produit: int, valides: int | None) -> dict:
    return {
        "produit": produit,
        "valides": valides,
        "taux_valide": None if valides is None else _taux(valides, produit),
        "dimensions": [
            {"nom": dimension, "n_alleles": len(valeurs(graphe, dimension))}
            for dimension in dimensions(graphe)
        ],
    }


def _point(
    candidat: dict,
    seuil: float,
    pareto_ids: set[str],
    frontiere: list[dict],
) -> dict:
    ids_front = {ligne["id"] for ligne in frontiere}
    utilites = {
        personne: detail["satisfaction_ajustee"]
        for personne, detail in (candidat.get("detail") or {}).items()
    }
    return {
        "id": candidat["id"],
        "choix": candidat.get("choix") or {},
        "least_misery": candidat["least_misery"],
        "moyenne": candidat["moyenne"],
        "penalite": candidat["penalite"],
        "dispersion": candidat["dispersion"],
        "acceptable": float(candidat["least_misery"]) >= seuil,
        "pareto": candidat["id"] in pareto_ids,
        "frontiere": candidat["id"] in ids_front,
        "falaise": float(candidat["penalite"]) > 0,
        "utilites": utilites,
    }


def _marginales(
    graphe: nx.MultiDiGraph,
    evalues: list[dict],
    seuil: float,
) -> list[dict]:
    """Meilleur least misery si l'on fixe un allèle.

    C'est ce qu'une mutation du génétique voit : certains gènes ne
    mènent jamais dans la région acceptable.
    """
    lignes = []
    for dimension in dimensions(graphe):
        for allele in valeurs(graphe, dimension):
            fixes = [
                candidat
                for candidat in evalues
                if (candidat.get("choix") or {}).get(dimension) == allele
            ]
            if not fixes:
                continue
            meilleur = max(float(candidat["least_misery"]) for candidat in fixes)
            n_acc = sum(
                1
                for candidat in fixes
                if float(candidat["least_misery"]) >= seuil
            )
            lignes.append(
                {
                    "dimension": dimension,
                    "allele": allele,
                    "n_valides": len(fixes),
                    "n_acceptables": n_acc,
                    "meilleur_least_misery": meilleur,
                }
            )
    return lignes


def _coupe(
    graphe: nx.MultiDiGraph,
    evalues: list[dict],
    seuil: float,
) -> dict | None:
    """Projection : pour deux axes, le meilleur least misery des autres gènes."""
    dims = dimensions(graphe)
    if len(dims) < 2:
        return None
    axes = sorted(
        dims,
        key=lambda dimension: (-len(valeurs(graphe, dimension)), dims.index(dimension)),
    )[:2]
    axe_x, axe_y = axes
    cellules = []
    for x in valeurs(graphe, axe_x):
        for y in valeurs(graphe, axe_y):
            fixes = [
                candidat
                for candidat in evalues
                if (candidat.get("choix") or {}).get(axe_x) == x
                and (candidat.get("choix") or {}).get(axe_y) == y
            ]
            if not fixes:
                cellules.append(
                    {
                        "x": x,
                        "y": y,
                        "n": 0,
                        "least_misery": None,
                        "acceptable": False,
                        "falaise": False,
                    }
                )
                continue
            meilleur = max(fixes, key=lambda candidat: float(candidat["least_misery"]))
            cellules.append(
                {
                    "x": x,
                    "y": y,
                    "n": len(fixes),
                    "least_misery": meilleur["least_misery"],
                    "acceptable": float(meilleur["least_misery"]) >= seuil,
                    "falaise": any(float(candidat["penalite"]) > 0 for candidat in fixes),
                }
            )
    return {"axe_x": axe_x, "axe_y": axe_y, "cellules": cellules}


def _voisins_valides(
    graphe: nx.MultiDiGraph,
    candidat: dict,
    par_id: dict[str, dict],
) -> list[dict]:
    choix = candidat.get("choix") or {}
    voisins = []
    for dimension in dimensions(graphe):
        for allele in valeurs(graphe, dimension):
            if allele == choix.get(dimension):
                continue
            autre = dict(choix)
            autre[dimension] = allele
            if not combinaison_valide(graphe, autre):
                continue
            identifiant = identifiant_candidat(graphe, autre)
            if identifiant in par_id and identifiant != candidat["id"]:
                voisins.append(par_id[identifiant])
    return voisins


def _a_un_voisin_invalide(graphe: nx.MultiDiGraph, choix: dict[str, str]) -> bool:
    for dimension in dimensions(graphe):
        for allele in valeurs(graphe, dimension):
            if allele == choix.get(dimension):
                continue
            autre = dict(choix)
            autre[dimension] = allele
            if not combinaison_valide(graphe, autre):
                return True
    return False


def _ids_pareto(evalues: list[dict]) -> set[str]:
    """Points non dominés dans l'espace des satisfactions ajustées.

    ``a`` domine ``b`` si chaque personne est au moins aussi satisfaite
    en ``a`` et une personne l'est strictement plus.
    """
    vecteurs = [(candidat["id"], _vecteur(candidat)) for candidat in evalues]
    retenus = set()
    for identifiant, vecteur in vecteurs:
        if not vecteur:
            continue
        domine = False
        for autre_id, autre in vecteurs:
            if autre_id == identifiant or not autre:
                continue
            if _domine(autre, vecteur):
                domine = True
                break
        if not domine:
            retenus.add(identifiant)
    return retenus


def _vecteur(candidat: dict) -> list[float]:
    detail = candidat.get("detail") or {}
    return [
        float(detail[personne]["satisfaction_ajustee"])
        for personne in sorted(detail)
    ]


def _domine(gauche: list[float], droite: list[float]) -> bool:
    if len(gauche) != len(droite) or not gauche:
        return False
    au_moins = all(a >= b for a, b in zip(gauche, droite))
    strict = any(a > b for a, b in zip(gauche, droite))
    return au_moins and strict


def _taux(partie: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return partie / total
