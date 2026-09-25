"""Charge un scénario (dict ou fichier JSON) en graphe NetworkX."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import networkx as nx

from agora.kr.schema import SCHEMA_SCENARIO


def charger(source: dict | str | Path) -> nx.MultiDiGraph:
    """Valide ``source`` et construit le graphe du domaine.

    ``source`` est soit le dict déjà parsé, soit un chemin de fichier JSON.
    Les extrémités de relation absentes des nœuds sont ajoutées comme
    concepts (``type="concept"``), pour que l'arête ait deux bouts.
    """
    scenario = source if isinstance(source, dict) else _lire_json(source)
    jsonschema.validate(scenario, SCHEMA_SCENARIO)
    return _construire(scenario)


def _lire_json(chemin: str | Path) -> dict:
    with Path(chemin).open(encoding="utf-8") as fichier:
        return json.load(fichier)


def _construire(scenario: dict) -> nx.MultiDiGraph:
    graphe = nx.MultiDiGraph()
    graphe.graph["id"] = scenario["id"]
    graphe.graph["domaine"] = scenario["domaine"]
    graphe.graph["dimensions"] = list(scenario["dimensions"])
    graphe.graph["participants"] = [dict(p) for p in scenario["participants"]]

    for noeud in scenario["noeuds"]:
        identifiant = noeud["id"]
        if identifiant in graphe:
            raise ValueError(f"nœud dupliqué : {identifiant}")
        graphe.add_node(
            identifiant,
            type=noeud["type"],
            label=noeud["label"],
            traits=list(noeud.get("traits") or []),
        )

    for relation in scenario["relations"]:
        for extremite in (relation["source"], relation["cible"]):
            if extremite not in graphe:
                graphe.add_node(
                    extremite,
                    type="concept",
                    label=extremite,
                    traits=[],
                )
        graphe.add_edge(
            relation["source"],
            relation["cible"],
            relation=relation["relation"],
        )
    return graphe
