"""Notes de base lues sur le graphe, sans nom de domaine en dur."""

from __future__ import annotations

from agora.kr.charger import charger
from agora.kr.requetes import dimensions, valeurs


def identifiant_participant(participant: dict | str) -> str:
    if isinstance(participant, str):
        return participant
    return participant["id"]


def borner(note: float) -> float:
    """Ramène une note sur l'échelle du contrat, -10 à +10."""
    return float(min(10.0, max(-10.0, float(note))))


def ids_domaine(scenario: dict) -> list[str]:
    """Valeurs des dimensions, plus les traits cités par ces nœuds."""
    return ids_depuis_graphe(charger(scenario))


def ids_depuis_graphe(graphe) -> list[str]:
    identifiants: list[str] = []
    for dimension in dimensions(graphe):
        for identifiant in valeurs(graphe, dimension):
            if identifiant not in identifiants:
                identifiants.append(identifiant)
    traits: list[str] = []
    for _noeud, data in graphe.nodes(data=True):
        for trait in data.get("traits") or []:
            if trait not in identifiants and trait not in traits:
                traits.append(trait)
    return identifiants + traits


def gout_groupe(
    scenario: dict,
    identifiants: list[str] | None = None,
) -> dict[str, float]:
    """Goût de groupe fourni par le scénario, ou moyenne des goûts.

    Les ids du domaine absents du dict reçoivent 0, pour que les
    profils complets aient une note de base partout.
    """
    if identifiants is None:
        identifiants = ids_domaine(scenario)
    explicite = scenario.get("gout_groupe")
    if explicite:
        base = {
            cle: float(valeur)
            for cle, valeur in explicite.items()
            if valeur is not None
        }
    else:
        sommes: dict[str, float] = {}
        comptes: dict[str, int] = {}
        for notes in (scenario.get("gouts") or {}).values():
            for cle, valeur in (notes or {}).items():
                if valeur is None:
                    continue
                sommes[cle] = sommes.get(cle, 0.0) + float(valeur)
                comptes[cle] = comptes.get(cle, 0) + 1
        base = {cle: sommes[cle] / comptes[cle] for cle in sommes}
    for identifiant in identifiants:
        base.setdefault(identifiant, 0.0)
    return base


def notes_de_base(
    participant: dict | str,
    scenario: dict,
    identifiants: list[str] | None = None,
) -> dict[str, float]:
    """Note de base d'une personne : son goût, sinon le goût de groupe."""
    if identifiants is None:
        identifiants = ids_domaine(scenario)
    pid = identifiant_participant(participant)
    personnelles = (scenario.get("gouts") or {}).get(pid) or {}
    groupe = gout_groupe(scenario, identifiants)
    notes = {}
    for identifiant in identifiants:
        if identifiant in personnelles and personnelles[identifiant] is not None:
            brut = personnelles[identifiant]
        else:
            brut = groupe.get(identifiant, 0.0)
        notes[identifiant] = borner(brut)
    return notes


def graine(seed: int, participant_id: str) -> int:
    """Graine stable, propre à la personne, sans ``hash()`` aléatoire."""
    acc = int(seed) & 0xFFFFFFFF
    for caractere in participant_id:
        acc = (acc * 16777619 + ord(caractere)) & 0xFFFFFFFF
    return acc
