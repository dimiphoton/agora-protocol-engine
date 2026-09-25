"""Ontologie de négociation, interrogée par la simulation.

Le graphe de domaine porte déjà les participants en métadonnée. Cette
couche y ajoute les classes (proposition, round, veto, clause, accord)
et les participants comme nœuds, puis les instances au fil des rounds.
Le moteur de scores ne lit pas ces nœuds : seule la boucle de
simulation les écrit et les relit.
"""

from __future__ import annotations

import networkx as nx

CLASSES = ("proposition", "round", "veto", "clause", "accord")


def poser_negociation(scenario: dict, graphe: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Pose les classes de négociation et un nœud par participant.

    Les classes ne sont pas des coquilles : chacune a un type, un
    libellé et un rôle. Les participants deviennent des nœuds
    ``type="participant"``, distincts des valeurs du domaine.
    """
    for nom in CLASSES:
        _assurer_classe(graphe, nom)
    for participant in scenario.get("participants") or []:
        pid = participant["id"]
        graphe.add_node(
            _noeud_participant(pid),
            type="participant",
            label=participant.get("label") or pid,
            participant_id=pid,
        )
    return graphe


def enregistrer_round(
    graphe: nx.MultiDiGraph,
    numero: int,
    meilleur_id: str | None,
    propositions: list[dict],
) -> str:
    """Ajoute un nœud round relié aux propositions de ce tour."""
    round_id = f"negociation:round:{int(numero)}"
    graphe.add_node(
        round_id,
        type="round",
        label=f"Round {int(numero)}",
        numero=int(numero),
        meilleur_id=meilleur_id,
    )
    _classer(graphe, round_id, "round")
    for index, proposition in enumerate(propositions):
        pid = proposition.get("participant_id") or str(index)
        prop_id = f"negociation:proposition:{int(numero)}:{pid}"
        graphe.add_node(
            prop_id,
            type="proposition",
            label=f"Proposition {pid}",
            participant_id=pid,
            notes=dict(proposition.get("notes") or {}),
            veto=list(proposition.get("veto") or []),
            round_numero=int(numero),
        )
        _classer(graphe, prop_id, "proposition")
        graphe.add_edge(round_id, prop_id, relation="contient")
        auteur = _noeud_participant(pid)
        if auteur in graphe:
            graphe.add_edge(prop_id, auteur, relation="auteur")
    return round_id


def enregistrer_veto(
    graphe: nx.MultiDiGraph,
    participant_id: str,
    cible_id: str,
    round_numero: int,
) -> str:
    """Enregistre un veto posé pendant un round, relié à sa cible."""
    veto_id = (
        f"negociation:veto:{int(round_numero)}:{participant_id}:{cible_id}"
    )
    graphe.add_node(
        veto_id,
        type="veto",
        label=f"Veto {cible_id}",
        participant_id=participant_id,
        cible_id=cible_id,
        round_numero=int(round_numero),
    )
    _classer(graphe, veto_id, "veto")
    round_id = f"negociation:round:{int(round_numero)}"
    if round_id in graphe:
        graphe.add_edge(round_id, veto_id, relation="contient")
    auteur = _noeud_participant(participant_id)
    if auteur in graphe:
        graphe.add_edge(veto_id, auteur, relation="auteur")
    if cible_id in graphe:
        graphe.add_edge(veto_id, cible_id, relation="cible")
    return veto_id


def cloturer_accord(graphe: nx.MultiDiGraph, meilleur: dict | None) -> str | None:
    """Crée l'accord et une clause par dimension du choix retenu.

    Le texte d'une clause est ``dimension = label`` du nœud choisi.
    """
    if not meilleur:
        return None
    accord_id = "negociation:accord"
    graphe.add_node(
        accord_id,
        type="accord",
        label="Accord",
        meilleur_id=meilleur.get("id"),
    )
    _classer(graphe, accord_id, "accord")
    choix = meilleur.get("choix") or {}
    for dimension in graphe.graph.get("dimensions") or []:
        if dimension not in choix:
            continue
        valeur = choix[dimension]
        label = _label(graphe, valeur)
        texte = f"{dimension} = {label}"
        clause_id = f"negociation:clause:{dimension}"
        graphe.add_node(
            clause_id,
            type="clause",
            label=texte,
            texte=texte,
            dimension=dimension,
            valeur=valeur,
        )
        _classer(graphe, clause_id, "clause")
        graphe.add_edge(accord_id, clause_id, relation="contient")
        if valeur in graphe:
            graphe.add_edge(clause_id, valeur, relation="retient")
    return accord_id


def lire_accord(graphe: nx.MultiDiGraph) -> dict | None:
    """Lit l'accord clos, ou ``None`` s'il n'y en a pas."""
    accords = [
        (identifiant, data)
        for identifiant, data in graphe.nodes(data=True)
        if data.get("type") == "accord"
    ]
    if not accords:
        return None
    identifiant, data = accords[0]
    clauses = []
    for _source, cible, _edge in graphe.out_edges(identifiant, data=True):
        if graphe.nodes[cible].get("type") != "clause":
            continue
        clause = graphe.nodes[cible]
        clauses.append(
            {
                "id": cible,
                "dimension": clause.get("dimension"),
                "valeur": clause.get("valeur"),
                "texte": clause.get("texte"),
            }
        )
    ordre = list(graphe.graph.get("dimensions") or [])
    if ordre:
        clauses.sort(
            key=lambda clause: (
                ordre.index(clause["dimension"])
                if clause["dimension"] in ordre
                else len(ordre)
            )
        )
    return {
        "id": identifiant,
        "meilleur_id": data.get("meilleur_id"),
        "clauses": clauses,
    }


def lire_rounds(graphe: nx.MultiDiGraph) -> list[dict]:
    """Rounds enregistrés, du premier au dernier, avec leurs propositions."""
    rounds = []
    for identifiant, data in graphe.nodes(data=True):
        if data.get("type") != "round":
            continue
        propositions = []
        for _source, cible, _edge in graphe.out_edges(identifiant, data=True):
            if graphe.nodes[cible].get("type") != "proposition":
                continue
            proposition = graphe.nodes[cible]
            propositions.append(
                {
                    "id": cible,
                    "participant_id": proposition.get("participant_id"),
                    "notes": dict(proposition.get("notes") or {}),
                    "veto": list(proposition.get("veto") or []),
                }
            )
        propositions.sort(key=lambda item: item.get("participant_id") or "")
        rounds.append(
            {
                "id": identifiant,
                "numero": data.get("numero"),
                "meilleur_id": data.get("meilleur_id"),
                "propositions": propositions,
            }
        )
    rounds.sort(key=lambda item: item.get("numero") or 0)
    return rounds


def _assurer_classe(graphe: nx.MultiDiGraph, nom: str) -> str:
    identifiant = f"negociation:classe:{nom}"
    if identifiant not in graphe:
        graphe.add_node(
            identifiant,
            type="classe",
            label=nom,
            role="negociation",
        )
    return identifiant


def _classer(graphe: nx.MultiDiGraph, instance_id: str, nom: str) -> None:
    graphe.add_edge(instance_id, _assurer_classe(graphe, nom), relation="sous_type")


def _noeud_participant(participant_id: str) -> str:
    return f"negociation:participant:{participant_id}"


def _label(graphe: nx.MultiDiGraph, identifiant: str) -> str:
    if identifiant in graphe:
        label = graphe.nodes[identifiant].get("label")
        if label:
            return str(label)
    return str(identifiant)
