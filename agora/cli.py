"""Ligne de commande du MVP Agora.

    python -m agora.cli scenarios
    python -m agora.cli run vacances_3 --simuler --seed 0
    python -m agora.cli run veto --prefs prefs.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agora.core.frontieres import analyser_frontieres
from agora.core.moteur import tourner
from agora.scenarios import charger_scenario, preferences_figees
from agora.simulateurs.boucle import jouer
from agora.version import version_git

# Libellés lisibles, dans l'ordre de l'interface.
CATALOGUE = (
    {"id": "vacances_3", "label": "Vacances, 3 personnes"},
    {"id": "vacances_large", "label": "Vacances, groupe large"},
    {"id": "resto", "label": "Restaurant"},
    {"id": "weekend", "label": "Week-end"},
    {"id": "unanimite", "label": "Limite : unanimité"},
    {"id": "conflit_total", "label": "Limite : conflit total"},
    {"id": "veto", "label": "Limite : veto"},
    {"id": "egalite", "label": "Limite : égalité"},
    {"id": "prefs_manquantes", "label": "Limite : préférences manquantes"},
)

GRAINE = 0


def lister_scenarios() -> list[dict]:
    """Scénarios connus, avec un libellé pour l'interface."""
    return [dict(item) for item in CATALOGUE]


def fusionner_preferences(base: dict | None, ajout: dict | None) -> dict:
    """Superpose ``ajout`` sur les préférences déjà écrites dans le scénario.

    Les notes se complètent. Le veto d'une personne présente dans
    ``ajout`` remplace celui de la base.
    """
    notes: dict[str, dict] = {}
    veto: dict[str, list] = {}
    for source, remplace_veto in ((base, False), (ajout, True)):
        if not source:
            continue
        for personne, contenu in (source.get("notes") or {}).items():
            bloc = notes.setdefault(str(personne), {})
            for cle, valeur in (contenu or {}).items():
                bloc[str(cle)] = valeur
        source_veto = source.get("veto")
        if not source_veto:
            continue
        for personne, cibles in source_veto.items():
            if remplace_veto or str(personne) not in veto:
                veto[str(personne)] = [str(cible) for cible in (cibles or [])]
    return {"notes": notes, "veto": veto}


def profils_pour(scenario: dict) -> dict[str, str]:
    """Profils du JSON, ou ``cooperatif`` si la personne n'en a pas."""
    declares = scenario.get("profils") or {}
    profils = {}
    for participant in scenario.get("participants") or []:
        identifiant = participant["id"]
        profils[identifiant] = declares.get(identifiant) or "cooperatif"
    return profils


def executer(
    nom: str,
    *,
    simuler: bool = False,
    seed: int = GRAINE,
    preferences: dict | None = None,
    fusionner: bool = True,
) -> dict:
    """Un round (``tourner``) ou une négociation (``jouer``), sans graphe."""
    scenario = charger_scenario(nom)
    if simuler:
        brut = jouer(scenario, profils_pour(scenario), seed=seed)
    else:
        if fusionner:
            prefs = fusionner_preferences(
                preferences_figees(scenario), preferences
            )
        else:
            prefs = preferences or {"notes": {}, "veto": {}}
        brut = tourner(scenario, prefs, seed=seed)
        brut["preferences"] = prefs
    return publier(nom, brut)


def publier(nom: str, brut: dict) -> dict:
    """Dict JSON : meilleur, historique, accord, mode, version. Pas de graphe."""
    return _serialisable(
        {
            "scenario": nom,
            "meilleur": brut.get("meilleur"),
            "classement": brut.get("classement") or [],
            "historique": brut.get("historique") or [],
            "accord": brut.get("accord"),
            "metriques": brut.get("metriques") or {},
            "mode": brut.get("mode"),
            "version": version_git(),
            "preferences": brut.get("preferences"),
            "chemins": brut.get("chemins"),
        }
    )


def lire_fichier_prefs(chemin: str) -> dict:
    """Lit ``{"notes": {...}, "veto": {...}}``."""
    path = Path(chemin)
    if not path.is_file():
        raise FileNotFoundError(
            f"fichier de préférences introuvable : {chemin}"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON illisible dans {chemin} : {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("le fichier de préférences doit être un objet JSON")
    return data


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée. 0 si le JSON est écrit, 1 si le scénario est inconnu."""
    parser = construire_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        if code is None or code == 0:
            return 0
        if isinstance(code, int):
            return code
        return 1

    try:
        if args.commande == "scenarios":
            payload = lister_scenarios()
        elif args.commande == "frontieres":
            payload = calculer_frontieres(
                args.scenario,
                seed=args.seed,
                simuler=args.simuler,
                seuil=args.seuil,
                preferences=lire_fichier_prefs(args.prefs) if args.prefs else None,
            )
        else:
            if args.simuler and args.prefs:
                raise ValueError("choisissez --simuler ou --prefs, pas les deux")
            preferences = (
                lire_fichier_prefs(args.prefs) if args.prefs else None
            )
            payload = executer(
                args.scenario,
                simuler=args.simuler,
                seed=args.seed,
                preferences=preferences,
            )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _sortie_utf8()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def construire_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m agora.cli",
        description="Compromis Agora, en ligne de commande.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "exemples :\n"
            "  python -m agora.cli scenarios\n"
            "  python -m agora.cli run vacances_3 --simuler --seed 0\n"
            "  python -m agora.cli run veto --prefs prefs.json"
        ),
    )
    sous = parser.add_subparsers(dest="commande", required=True)
    sous.add_parser("scenarios", help="liste les scénarios")
    lancer = sous.add_parser("run", help="calcule un compromis")
    lancer.add_argument("scenario", help="nom du scénario, par exemple veto")
    lancer.add_argument(
        "--simuler",
        action="store_true",
        help="joue la négociation avec les profils du scénario",
    )
    lancer.add_argument("--seed", type=int, default=GRAINE)
    lancer.add_argument(
        "--prefs",
        help="fichier JSON {notes, veto} pour un seul round",
    )
    carte = sous.add_parser(
        "frontieres",
        help="espace valide, région acceptable, Pareto, falaise de veto",
    )
    carte.add_argument("scenario", help="nom du scénario")
    carte.add_argument("--seuil", type=float, default=0.0)
    carte.add_argument("--simuler", action="store_true")
    carte.add_argument("--seed", type=int, default=GRAINE)
    carte.add_argument("--prefs", help="fichier JSON {notes, veto}")
    return parser


def calculer_frontieres(
    nom: str,
    *,
    seed: int = GRAINE,
    simuler: bool = False,
    seuil: float = 0.0,
    preferences: dict | None = None,
) -> dict:
    """Paysage du scénario, sans le graphe NetworkX."""
    scenario = charger_scenario(nom)
    if simuler:
        brut = jouer(scenario, profils_pour(scenario), seed=seed)
        prefs = brut.get("preferences") or {"notes": {}, "veto": {}}
    else:
        prefs = fusionner_preferences(preferences_figees(scenario), preferences)
    paysage = analyser_frontieres(scenario, prefs, seuil=seuil)
    paysage["scenario"] = nom
    paysage["version"] = version_git()
    return _serialisable(paysage)


def _serialisable(valeur):
    """Types JSON. Une clé ``graphe`` est retirée à tous les niveaux."""
    if valeur is None or type(valeur) in (str, int, float, bool):
        return valeur
    if isinstance(valeur, dict):
        return {
            str(cle): _serialisable(item)
            for cle, item in valeur.items()
            if cle != "graphe"
        }
    if isinstance(valeur, (list, tuple)):
        return [_serialisable(item) for item in valeur]
    if hasattr(valeur, "item") and callable(valeur.item):
        try:
            return _serialisable(valeur.item())
        except ValueError:
            pass
    raise TypeError(f"objet non sérialisable : {type(valeur).__name__}")


def _sortie_utf8() -> None:
    for flux in (sys.stdout, sys.stderr):
        reconfigurer = getattr(flux, "reconfigure", None)
        if reconfigurer is None:
            continue
        try:
            reconfigurer(encoding="utf-8")
        except (OSError, ValueError):
            continue


if __name__ == "__main__":
    sys.exit(main())
