"""Chemins de négociation testés sur le graphe.

Le graphe de départ décrit le domaine. Chaque essai ajoute des nœuds
``chemin`` et, pour l'essai retenu, un nœud ``direction``. Le graphe
grossit avec les conversations : on relit ces nœuds, on ne les garde
pas dans un tableau à part.

Trois sortes d'essais :

- ``proposer`` : un voisin valide (un seul gène changé). Gain = hausse
  du least misery.
- ``conceder`` : on retire un veto le temps du test. Gain = hausse du
  least misery si ce refus devient négociable.
- ``questionner`` : une case vide. On essaie les notes +10 et -10.
  Le gain est l'écart entre les deux least misery : la case peut
  encore faire bouger le consensus.

La direction retenue est l'essai au gain le plus haut. À gain nul,
on tient le candidat actuel (``tenir``).
"""

from __future__ import annotations

import networkx as nx

from agora.core.evaluation import evaluer_candidat
from agora.core.exploration import explorer
from agora.core.scores import fitness_key
from agora.kr.requetes import (
    candidat_depuis_choix,
    combinaison_valide,
    dimensions,
    etendre_preferences,
    participants,
    valeurs,
)

MAX_VOISINS = 16
MAX_QUESTIONS = 8


def essayer_chemins(
    graphe: nx.MultiDiGraph,
    preferences: dict,
    numero: int = 1,
    seed: int = 0,
) -> dict:
    """Teste des chemins et écrit le résultat dans le graphe."""
    classement = _classement(graphe, preferences, seed)
    actuel = classement[0] if classement else None
    essais = _essais(graphe, preferences, actuel, classement)
    if not essais:
        retenu = {
            "type": "tenir",
            "gain": 0.0,
            "least_misery": _lm(actuel),
            "detail": "aucun chemin ne bouge le least misery",
        }
    else:
        # Un vrai progrès (proposition ou concession) passe avant une question.
        # La question ne change pas encore le score : elle mesure une sensibilité.
        progres = [
            essai
            for essai in essais
            if essai["type"] in ("proposer", "conceder") and essai["gain"] > 0
        ]
        progres.sort(key=lambda essai: (-essai["gain"], essai["type"]))
        if progres:
            retenu = progres[0]
        else:
            questions = [essai for essai in essais if essai["type"] == "questionner"]
            questions.sort(key=lambda essai: -essai["gain"])
            if questions and questions[0]["gain"] > 0:
                retenu = questions[0]
            else:
                retenu = {
                    "type": "tenir",
                    "gain": 0.0,
                    "least_misery": _lm(actuel),
                    "detail": "les chemins testés n'améliorent pas le least misery",
                }
    _ecrire(graphe, numero, essais, retenu, actuel)
    return {
        "retenu": _sans_interne(retenu),
        "testes": [_sans_interne(essai) for essai in essais],
        "n_noeuds": graphe.number_of_nodes(),
    }


def lire_chemins(graphe: nx.MultiDiGraph) -> list[dict]:
    """Chemins écrits dans le graphe, du premier tour au dernier."""
    lignes = []
    for identifiant, data in graphe.nodes(data=True):
        if data.get("type") != "chemin":
            continue
        lignes.append(
            {
                "id": identifiant,
                "numero": data.get("numero"),
                "type_chemin": data.get("type_chemin"),
                "gain": data.get("gain"),
                "detail": data.get("detail"),
                "retenu": bool(data.get("retenu")),
            }
        )
    lignes.sort(key=lambda ligne: (ligne["numero"] or 0, ligne["id"]))
    return lignes


def lire_direction(graphe: nx.MultiDiGraph, numero: int) -> dict | None:
    """Direction retenue pour un tour, lue sur le graphe."""
    for identifiant, data in graphe.nodes(data=True):
        if data.get("type") != "direction":
            continue
        if data.get("numero") != int(numero):
            continue
        return {
            "id": identifiant,
            "type": data.get("type_chemin"),
            "gain": data.get("gain"),
            "detail": data.get("detail"),
        }
    return None


def _essais(graphe, preferences, actuel, classement: list[dict]) -> list[dict]:
    essais = []
    essais.extend(_voisins(graphe, preferences, actuel))
    essais.extend(_concessions(graphe, preferences, actuel, classement))
    essais.extend(_questions(graphe, preferences, actuel, classement))
    return essais


def _voisins(graphe, preferences, actuel) -> list[dict]:
    if not actuel:
        return []
    choix = actuel.get("choix") or {}
    base = _lm(actuel)
    essais = []
    for autre in _choix_voisins(graphe, choix):
        note = _evaluer_choix(graphe, preferences, autre)
        candidat_id = note["id"]
        essais.append(
            {
                "type": "proposer",
                "gain": _lm(note) - base,
                "least_misery": _lm(note),
                "cible": candidat_id,
                "detail": f"proposer {candidat_id}",
            }
        )
        if len(essais) >= MAX_VOISINS:
            break
    return essais


def _concessions(graphe, preferences, actuel, classement: list[dict]) -> list[dict]:
    base = _lm(actuel)
    veto = preferences.get("veto") or {}
    essais = []
    vus = set()
    for personne, cibles in veto.items():
        for cible in cibles or []:
            cle = (personne, cible)
            if cle in vus:
                continue
            vus.add(cle)
            hypothese = _sans_veto(preferences, personne, cible)
            note = _meilleur_connu(graphe, hypothese, classement)
            essais.append(
                {
                    "type": "conceder",
                    "gain": _lm(note) - base,
                    "least_misery": _lm(note),
                    "personne": personne,
                    "cible": cible,
                    "detail": f"rendre négociable le veto de {personne} sur {cible}",
                }
            )
            if len(essais) >= MAX_VOISINS:
                return essais
    return essais


def _questions(graphe, preferences, actuel, classement: list[dict]) -> list[dict]:
    if not actuel:
        return []
    notes = preferences.get("notes") or {}
    personnes = [p["id"] for p in participants(graphe)]
    # D'abord la personne la moins satisfaite du candidat actuel.
    detail = actuel.get("detail") or {}
    personnes.sort(
        key=lambda pid: float((detail.get(pid) or {}).get("satisfaction_ajustee", 0.0))
    )
    attributs = list((actuel.get("choix") or {}).values())
    essais = []
    for personne in personnes:
        deja = notes.get(personne) or {}
        for attribut in attributs:
            if attribut in deja and deja[attribut] is not None:
                continue
            haut = _avec_note(preferences, personne, attribut, 10)
            bas = _avec_note(preferences, personne, attribut, -10)
            ecart = abs(
                _lm(_meilleur_connu(graphe, haut, classement))
                - _lm(_meilleur_connu(graphe, bas, classement))
            )
            essais.append(
                {
                    "type": "questionner",
                    "gain": ecart,
                    "personne": personne,
                    "cible": attribut,
                    "detail": f"demander à {personne} une note sur {attribut}",
                }
            )
            if len(essais) >= MAX_QUESTIONS:
                return essais
    return essais


def _choix_voisins(graphe: nx.MultiDiGraph, choix: dict) -> list[dict]:
    voisins = []
    for dimension in dimensions(graphe):
        for allele in valeurs(graphe, dimension):
            if allele == choix.get(dimension):
                continue
            autre = dict(choix)
            autre[dimension] = allele
            if combinaison_valide(graphe, autre):
                voisins.append(autre)
    return voisins


def _evaluer_choix(graphe, preferences: dict, choix: dict) -> dict:
    candidat = candidat_depuis_choix(graphe, choix)
    etendues = etendre_preferences(graphe, preferences)
    ids = [personne["id"] for personne in participants(graphe)]
    note = evaluer_candidat(
        candidat,
        ids,
        etendues["notes"],
        etendues["veto"],
        graphe,
    )
    return {**candidat, **note}


def _meilleur_connu(graphe, preferences: dict, classement: list[dict]) -> dict | None:
    """Reprend les génomes déjà vus et les re-note sous une hypothèse."""
    if not classement:
        return None
    notes = [
        _evaluer_choix(graphe, preferences, candidat["choix"])
        for candidat in classement
        if candidat.get("choix")
    ]
    if not notes:
        return None
    notes.sort(key=fitness_key)
    return notes[0]


def _classement(graphe, preferences: dict, seed: int) -> list[dict]:
    etendues = etendre_preferences(graphe, preferences)
    ids = [personne["id"] for personne in participants(graphe)]

    def evaluer(candidat: dict) -> dict:
        return evaluer_candidat(
            candidat,
            ids,
            etendues["notes"],
            etendues["veto"],
            graphe,
        )

    exploration = explorer(graphe, evaluer, seed=seed)
    classement = list(exploration["classement"])
    classement.sort(key=fitness_key)
    return classement


def _sans_veto(preferences: dict, personne: str, cible: str) -> dict:
    notes = {
        pid: dict(contenu or {})
        for pid, contenu in (preferences.get("notes") or {}).items()
    }
    veto = {}
    for pid, cibles in (preferences.get("veto") or {}).items():
        if pid == personne:
            veto[pid] = [item for item in (cibles or []) if item != cible]
        else:
            veto[pid] = list(cibles or [])
    return {"notes": notes, "veto": veto}


def _avec_note(preferences: dict, personne: str, attribut: str, note: float) -> dict:
    notes = {
        pid: dict(contenu or {})
        for pid, contenu in (preferences.get("notes") or {}).items()
    }
    notes.setdefault(personne, {})[attribut] = note
    veto = {
        pid: list(cibles or [])
        for pid, cibles in (preferences.get("veto") or {}).items()
    }
    return {"notes": notes, "veto": veto}


def _ecrire(graphe, numero: int, essais: list[dict], retenu: dict, actuel: dict | None) -> None:
    tour_id = f"negociation:conversation:{int(numero)}"
    graphe.add_node(
        tour_id,
        type="conversation",
        label=f"Conversation {int(numero)}",
        numero=int(numero),
        meilleur_id=None if not actuel else actuel.get("id"),
    )
    for index, essai in enumerate(essais):
        chemin_id = f"negociation:chemin:{int(numero)}:{index}"
        graphe.add_node(
            chemin_id,
            type="chemin",
            label=essai["detail"],
            numero=int(numero),
            type_chemin=essai["type"],
            gain=float(essai["gain"]),
            detail=essai["detail"],
            retenu=False,
        )
        graphe.add_edge(tour_id, chemin_id, relation="teste")
        cible = essai.get("cible")
        if cible in graphe:
            graphe.add_edge(chemin_id, cible, relation="vise")
    direction_id = f"negociation:direction:{int(numero)}"
    graphe.add_node(
        direction_id,
        type="direction",
        label=retenu["detail"],
        numero=int(numero),
        type_chemin=retenu["type"],
        gain=float(retenu["gain"]),
        detail=retenu["detail"],
    )
    graphe.add_edge(tour_id, direction_id, relation="retient")
    # Marque le chemin retenu quand il correspond à un essai écrit.
    for index, essai in enumerate(essais):
        if essai["type"] == retenu["type"] and essai["detail"] == retenu["detail"]:
            chemin_id = f"negociation:chemin:{int(numero)}:{index}"
            graphe.nodes[chemin_id]["retenu"] = True
            graphe.add_edge(direction_id, chemin_id, relation="choisit")


def _lm(candidat: dict | None) -> float:
    if not candidat:
        return 0.0
    return float(candidat.get("least_misery") or 0.0)


def _sans_interne(essai: dict) -> dict:
    return {
        cle: valeur
        for cle, valeur in essai.items()
        if cle != "meilleur_essai"
    }
