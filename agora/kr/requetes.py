"""Seul accès du moteur au graphe.

Les fonctions ci-dessous lisent le MultiDiGraph produit par ``charger``.
Le reste du moteur ne parcourt pas les arêtes lui-même.
"""

from __future__ import annotations

import itertools
from collections import deque

import networkx as nx

# Une arête de ce type, d'un nœud choisi vers T, satisfait « A requiert T ».
RELATIONS_FOURNIT = frozenset({"fournit", "a", "porte", "a_trait", "possede"})


def dimensions(graphe: nx.MultiDiGraph) -> list[str]:
    """Noms des dimensions, dans l'ordre du scénario."""
    return list(graphe.graph.get("dimensions", []))


def participants(graphe: nx.MultiDiGraph) -> list[dict]:
    """Participants déclarés dans le scénario (``id``, ``label``)."""
    return [dict(p) for p in graphe.graph.get("participants", [])]


def valeurs(graphe: nx.MultiDiGraph, dimension: str) -> list[str]:
    """Identifiants des nœuds dont le type est ``dimension``.

    L'ordre est celui de l'insertion dans le graphe (l'ordre du JSON).
    """
    return [
        identifiant
        for identifiant, data in graphe.nodes(data=True)
        if data.get("type") == dimension
    ]


def combinaison_valide(graphe: nx.MultiDiGraph, choix: dict[str, str]) -> bool:
    """Une valeur par dimension, et les contraintes du graphe tiennent.

    ``requiert`` : la cible T est un id choisi, ou un nœud choisi porte T
    dans ses traits, ou une relation de fourniture relie un nœud choisi à T.
    ``incompatible`` : si les deux extrémités sont présentes (id ou trait),
    la combinaison est rejetée.
    """
    dims = dimensions(graphe)
    if any(dim not in choix for dim in dims):
        return False
    for dim in dims:
        if choix[dim] not in valeurs(graphe, dim):
            return False
    retenus = [choix[dim] for dim in dims]
    if not _requiert_satisfaits(graphe, retenus):
        return False
    if _a_une_incompatibilite(graphe, retenus):
        return False
    return True


def enumerer_candidats(
    graphe: nx.MultiDiGraph,
    limite: int | None = None,
) -> list[dict]:
    """Produit cartésien des valeurs, filtré par ``combinaison_valide``.

    Chaque candidat a un ``id`` stable (dimensions dans l'ordre du scénario)
    et un ``choix`` ``{dimension: id}``.

    ``limite`` coupe le parcours dès ce nombre de candidats valides.
    L'exploration s'en sert pour détecter un espace au-dessus du seuil
    sans construire tout le produit.
    """
    dims = dimensions(graphe)
    if not dims:
        return []
    listes = [valeurs(graphe, dim) for dim in dims]
    if any(not liste for liste in listes):
        return []

    candidats = []
    for combo in itertools.product(*listes):
        choix = {dim: combo[index] for index, dim in enumerate(dims)}
        if not combinaison_valide(graphe, choix):
            continue
        candidats.append(candidat_depuis_choix(graphe, choix))
        if limite is not None and len(candidats) >= limite:
            break
    return candidats


def candidat_depuis_choix(
    graphe: nx.MultiDiGraph,
    choix: dict[str, str],
) -> dict:
    """Candidat ``{id, choix}`` pour un choix déjà complet."""
    dims = dimensions(graphe)
    choix_ordonne = {dim: choix[dim] for dim in dims}
    identifiant = identifiant_candidat(graphe, choix_ordonne)
    return {"id": identifiant, "choix": choix_ordonne}


def identifiant_candidat(
    graphe: nx.MultiDiGraph,
    choix: dict[str, str],
) -> str:
    """Id stable : ``dimension=valeur`` joints par ``|``.

    L'ordre est celui des dimensions du scénario.
    """
    return "|".join(f"{dim}={choix[dim]}" for dim in dimensions(graphe))


def etendre_preferences(graphe: nx.MultiDiGraph, prefs: dict) -> dict:
    """Recopie les notes et complète les nœuds sans note propre.

    Priorité, uniquement si le nœud n'a pas de note propre :

    1. ``sous_type`` : note de l'ancêtre le plus proche (à distance égale,
       l'identifiant le plus petit) ;
    2. ``implique`` : note de la conséquence la plus proche (même départage) ;
    3. traits : moyenne des notes posées sur les traits du nœud.

    Une note sur une classe parente ou sur un trait est donc autorisée.
    Les veto sont recopiés tels quels : le décompte se fait à l'évaluation.
    """
    notes_in = prefs.get("notes") or {}
    veto_in = prefs.get("veto") or {}
    # dict.fromkeys garde le premier ordre rencontré (pas le hasard d'un set).
    personnes = list(dict.fromkeys([*notes_in, *veto_in]))

    notes_out: dict[str, dict[str, float]] = {}
    for personne in personnes:
        directes = {
            cle: float(valeur)
            for cle, valeur in (notes_in.get(personne) or {}).items()
            if valeur is not None
        }
        etendues = dict(directes)
        for noeud in graphe.nodes:
            if noeud in directes:
                continue
            heritee = _note_la_plus_proche(
                graphe, noeud, directes, "sous_type"
            )
            if heritee is None:
                heritee = _note_la_plus_proche(
                    graphe, noeud, directes, "implique"
                )
            if heritee is None:
                heritee = _note_des_traits(graphe, noeud, directes)
            if heritee is not None:
                etendues[noeud] = heritee
        notes_out[personne] = etendues

    veto_out = {
        personne: list(veto_in.get(personne) or [])
        for personne in personnes
    }
    return {"notes": notes_out, "veto": veto_out}


def compter_veto(
    graphe: nx.MultiDiGraph | None,
    choix: dict[str, str],
    veto_ids: list[str],
) -> int:
    """Nombre de veto de la liste qui touchent le choix.

    Sans graphe, seul l'identifiant choisi compte. Avec graphe, un veto
    touche aussi un trait du choix, un ancêtre ``sous_type`` ou une
    conséquence ``implique``.
    """
    return sum(
        1 for veto_id in veto_ids if veto_touche(graphe, choix, veto_id)
    )


def veto_touche(
    graphe: nx.MultiDiGraph | None,
    choix: dict[str, str],
    veto_id: str,
) -> bool:
    """Vrai si ``veto_id`` est présent dans le choix, directement ou inféré."""
    choisis = list(choix.values())
    if veto_id in choisis:
        return True
    if graphe is None:
        return False
    for noeud in choisis:
        if noeud not in graphe:
            continue
        traits = graphe.nodes[noeud].get("traits") or []
        if veto_id in traits:
            return True
        if veto_id in _atteignables(graphe, noeud, "sous_type"):
            return True
        if veto_id in _atteignables(graphe, noeud, "implique"):
            return True
    return False


def _requiert_satisfaits(graphe: nx.MultiDiGraph, retenus: list[str]) -> bool:
    for source in retenus:
        for cible in _cibles(graphe, source, frozenset({"requiert"})):
            if not any(_porte(graphe, noeud, cible) for noeud in retenus):
                return False
    return True


def _porte(graphe: nx.MultiDiGraph, noeud: str, trait: str) -> bool:
    if noeud == trait:
        return True
    if noeud not in graphe:
        return False
    if trait in (graphe.nodes[noeud].get("traits") or []):
        return True
    return trait in _cibles(graphe, noeud, RELATIONS_FOURNIT)


def _a_une_incompatibilite(
    graphe: nx.MultiDiGraph,
    retenus: list[str],
) -> bool:
    presents = set(retenus)
    for noeud in retenus:
        if noeud in graphe:
            presents.update(graphe.nodes[noeud].get("traits") or [])
    for source, cible, data in graphe.edges(data=True):
        if data.get("relation") != "incompatible":
            continue
        if source in presents and cible in presents:
            return True
    return False


def _cibles(
    graphe: nx.MultiDiGraph,
    source: str,
    relations: frozenset[str],
) -> list[str]:
    if source not in graphe:
        return []
    trouvees = []
    for _, cible, data in graphe.out_edges(source, data=True):
        if data.get("relation") in relations:
            trouvees.append(cible)
    return trouvees


def _atteignables(
    graphe: nx.MultiDiGraph,
    depart: str,
    relation: str,
) -> set[str]:
    """Nœuds atteints en suivant ``relation`` (le départ est exclu)."""
    vus = {depart}
    file: deque[str] = deque(_cibles(graphe, depart, frozenset({relation})))
    atteints: set[str] = set()
    while file:
        courant = file.popleft()
        if courant in vus:
            continue
        vus.add(courant)
        atteints.add(courant)
        file.extend(_cibles(graphe, courant, frozenset({relation})))
    return atteints


def _note_la_plus_proche(
    graphe: nx.MultiDiGraph,
    depart: str,
    directes: dict[str, float],
    relation: str,
) -> float | None:
    """Note directe la plus proche en suivant ``relation`` vers l'extérieur."""
    vus = {depart}
    niveau = [
        voisin
        for voisin in _cibles(graphe, depart, frozenset({relation}))
        if voisin not in vus
    ]
    for voisin in niveau:
        vus.add(voisin)

    while niveau:
        porteurs = [noeud for noeud in niveau if noeud in directes]
        if porteurs:
            return float(directes[min(porteurs)])
        suivant = []
        for noeud in niveau:
            for voisin in _cibles(graphe, noeud, frozenset({relation})):
                if voisin not in vus:
                    vus.add(voisin)
                    suivant.append(voisin)
        niveau = suivant
    return None


def _note_des_traits(
    graphe: nx.MultiDiGraph,
    noeud: str,
    directes: dict[str, float],
) -> float | None:
    if noeud not in graphe:
        return None
    notes = [
        float(directes[trait])
        for trait in graphe.nodes[noeud].get("traits") or []
        if trait in directes
    ]
    if not notes:
        return None
    return sum(notes) / len(notes)
