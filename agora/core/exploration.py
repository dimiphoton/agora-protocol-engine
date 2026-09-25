"""Exploration exhaustive ou génétique des combinaisons valides."""

from __future__ import annotations

import random

import networkx as nx

from agora.core.scores import fitness_key
from agora.kr.requetes import (
    candidat_depuis_choix,
    combinaison_valide,
    dimensions,
    enumerer_candidats,
    valeurs,
)

# Au-delà, l'énumération cède la place à l'algorithme génétique.
SEUIL_EXHAUSTIF = 2000
TAILLE_POPULATION = 40
MAX_GENERATIONS = 40
STAGNATION_MAX = 8


def explorer(graphe: nx.MultiDiGraph, evaluer, seed: int = 0) -> dict:
    """Classe les candidats valides.

    Si ``len(enumerer_candidats) <= SEUIL_EXHAUSTIF``, tous sont évalués.
    Sinon, ``genetique`` cherche dans les combinaisons valides.
    ``evaluer(candidat)`` renvoie les agrégats (least_misery, moyenne, ...).
    """
    # +1 pour distinguer « exactement le seuil » de « au-dessus ».
    candidats = enumerer_candidats(graphe, limite=SEUIL_EXHAUSTIF + 1)
    if len(candidats) <= SEUIL_EXHAUSTIF:
        classement = _evaluer_et_trier(candidats, evaluer)
        meilleur = classement[0] if classement else None
        return {
            "mode": "exhaustif",
            "classement": classement,
            "meilleur": meilleur,
        }

    evolution = _evolution(graphe, evaluer, seed)
    return {
        "mode": "genetique",
        "classement": evolution["classement"],
        "meilleur": evolution["meilleur"],
    }


def genetique(graphe: nx.MultiDiGraph, evaluer, seed: int = 0) -> dict | None:
    """Meilleur candidat trouvé par l'algorithme génétique.

    Population 40, 40 générations au plus, arrêt si la meilleure fitness
    ne progresse pas pendant 8 générations. Deux individus d'élite sont
    gardés. La moitié des autres est un tirage valide au hasard, l'autre
    moitié un croisement puis une mutation, réparés pour rester dans les
    combinaisons valides. ``seed`` fixe le hasard.
    """
    return _evolution(graphe, evaluer, seed)["meilleur"]


def _evaluer_et_trier(candidats: list[dict], evaluer) -> list[dict]:
    evalues = []
    for candidat in candidats:
        evalues.append({**candidat, **evaluer(candidat)})
    evalues.sort(key=fitness_key)
    return evalues


def _evolution(graphe: nx.MultiDiGraph, evaluer, seed: int) -> dict:
    rng = random.Random(seed)
    dims = dimensions(graphe)
    alleles = {dim: list(valeurs(graphe, dim)) for dim in dims}
    if not dims or any(not alleles[dim] for dim in dims):
        return {"meilleur": None, "classement": []}

    vus: dict[str, dict] = {}

    def evaluer_choix(choix: dict[str, str]) -> dict:
        candidat = candidat_depuis_choix(graphe, choix)
        if candidat["id"] in vus:
            return vus[candidat["id"]]
        evalue = {**candidat, **evaluer(candidat)}
        vus[candidat["id"]] = evalue
        return evalue

    population = []
    tentatives = 0
    doublons = 0
    plafond = TAILLE_POPULATION * 40
    while len(population) < TAILLE_POPULATION and tentatives < plafond:
        tentatives += 1
        choix = _genome_aleatoire(rng, graphe, dims, alleles)
        if choix is None:
            break
        individu = evaluer_choix(choix)
        deja_la = any(
            individu["id"] == present["id"] for present in population
        )
        if deja_la:
            doublons += 1
            # L'espace valide est plus petit que la population.
            if doublons >= 40:
                break
            continue
        doublons = 0
        population.append(individu)
    if not population and _produit_alleles(alleles) <= SEUIL_EXHAUSTIF:
        for candidat in enumerer_candidats(graphe)[:TAILLE_POPULATION]:
            population.append(evaluer_choix(candidat["choix"]))
    if not population:
        return {"meilleur": None, "classement": []}

    population.sort(key=fitness_key)
    meilleur = population[0]
    sans_progres = 0

    for _generation in range(MAX_GENERATIONS):
        suivant = population[:2] if len(population) >= 2 else population[:1]
        while len(suivant) < TAILLE_POPULATION:
            if rng.random() < 0.5:
                choix = _genome_aleatoire(rng, graphe, dims, alleles)
            else:
                premier = _tournoi(rng, population)
                second = _tournoi(rng, population)
                enfant = _croiser(rng, graphe, dims, alleles, premier, second)
                choix = _muter(rng, graphe, dims, alleles, enfant)
            if choix is None:
                break
            suivant.append(evaluer_choix(choix))
        if len(suivant) <= len(population[:1]):
            break
        population = sorted(suivant, key=fitness_key)[:TAILLE_POPULATION]
        courant = population[0]
        if fitness_key(courant) < fitness_key(meilleur):
            meilleur = courant
            sans_progres = 0
        else:
            sans_progres += 1
            if sans_progres >= STAGNATION_MAX:
                break

    classement = sorted(vus.values(), key=fitness_key)
    meilleur = classement[0] if classement else meilleur
    return {"meilleur": meilleur, "classement": classement}


def _produit_alleles(alleles: dict[str, list[str]]) -> int:
    produit = 1
    for options in alleles.values():
        produit *= max(len(options), 1)
    return produit


def _tournoi(rng: random.Random, population: list[dict]) -> dict[str, str]:
    taille = min(3, len(population))
    pretendants = rng.sample(population, taille)
    pretendants.sort(key=fitness_key)
    return dict(pretendants[0]["choix"])


def _genome_aleatoire(
    rng: random.Random,
    graphe: nx.MultiDiGraph,
    dims: list[str],
    alleles: dict[str, list[str]],
) -> dict[str, str] | None:
    for _ in range(400):
        choix = {dim: rng.choice(alleles[dim]) for dim in dims}
        if combinaison_valide(graphe, choix):
            return choix
    return None


def _croiser(
    rng: random.Random,
    graphe: nx.MultiDiGraph,
    dims: list[str],
    alleles: dict[str, list[str]],
    parent_a: dict[str, str],
    parent_b: dict[str, str],
) -> dict[str, str]:
    enfant = {
        dim: parent_a[dim] if rng.random() < 0.5 else parent_b[dim]
        for dim in dims
    }
    if combinaison_valide(graphe, enfant):
        return enfant
    for _ in range(40):
        essai = dict(enfant)
        dim = rng.choice(dims)
        essai[dim] = rng.choice(alleles[dim])
        if combinaison_valide(graphe, essai):
            return essai
    if combinaison_valide(graphe, parent_a):
        return dict(parent_a)
    return dict(parent_b)


def _muter(
    rng: random.Random,
    graphe: nx.MultiDiGraph,
    dims: list[str],
    alleles: dict[str, list[str]],
    choix: dict[str, str],
) -> dict[str, str]:
    mutant = dict(choix)
    for dim in dims:
        if rng.random() > 0.4:
            continue
        options = [valeur for valeur in alleles[dim] if valeur != mutant[dim]]
        rng.shuffle(options)
        for option in options:
            essai = dict(mutant)
            essai[dim] = option
            if combinaison_valide(graphe, essai):
                mutant = essai
                break
    return mutant
