"""Chargement des scénarios JSON du MVP."""

from __future__ import annotations

import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent


def charger_scenario(nom: str) -> dict:
    """Lit ``agora/scenarios/<nom>.json`` ou ``limites/<nom>.json``."""
    with _chemin(nom).open(encoding="utf-8") as fichier:
        return json.load(fichier)


def preferences_figees(scenario: dict) -> dict | None:
    """Préférences écrites dans le JSON, ou ``None`` s'il n'y en a pas.

    Les cas limites s'en servent pour appeler ``tourner`` sans simulateur.
    """
    if "preferences" not in scenario or scenario["preferences"] is None:
        return None
    prefs = scenario["preferences"]
    notes = {
        personne: dict(contenu or {})
        for personne, contenu in (prefs.get("notes") or {}).items()
    }
    veto = {
        personne: list(cibles or [])
        for personne, cibles in (prefs.get("veto") or {}).items()
    }
    return {"notes": notes, "veto": veto}


def _chemin(nom: str) -> Path:
    relatif = nom[:-5] if nom.endswith(".json") else nom
    direct = (RACINE / relatif).with_suffix(".json")
    if direct.is_file():
        return direct
    limites = RACINE / "limites" / f"{Path(relatif).name}.json"
    if limites.is_file():
        return limites
    raise FileNotFoundError(f"scénario introuvable : {nom}")
