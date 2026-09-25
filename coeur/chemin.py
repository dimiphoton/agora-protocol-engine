"""Recherche de consensus : des pas autorisés, écrits dans le graphe.

SPARQL lit l'état. Le choix du pas est du Python. Chaque essai devient
un nœud ``Chemin``. La direction retenue est un nœud ``Direction``.
"""

from __future__ import annotations

from coeur.criteres import evaluer, meilleur
from coeur.graphe import ajouter_lien, ajouter_noeud
from coeur.requetes import executer
from coeur.regles import lire_regles
from coeur.session import Session
from coeur.sondage import sonder
from coeur.succes import lire_succes


def chercher_consensus(session: Session) -> dict:
    """Enchaîne des tours jusqu'au critère d'arrêt."""
    regles = lire_regles(session)
    succes = lire_succes(session)
    historique = []
    precedent = None
    stable = 0
    for tour in range(1, succes["max_tours"] + 1):
        session.tour = tour
        bilan = _tour(session, regles, succes)
        historique.append(bilan)
        if bilan["meilleur"] == precedent:
            stable += 1
        else:
            stable = 1
            precedent = bilan["meilleur"]
        if stable >= succes["tours_stables"]:
            break
    return {
        "meilleur": precedent,
        "tours": len(historique),
        "historique": historique,
        "chemins": executer(session, "chemins"),
    }


def _tour(session: Session, regles: dict, succes: dict) -> dict:
    etat = _etat(session)
    scores = _scores(etat, regles, blocage=regles["mode_veto"] == "blocage")
    choisi = meilleur(scores, succes["critere"])
    essais = _essais(session, etat, scores, choisi, regles, succes)
    retenu = _choisir(essais, choisi, scores, succes)
    _ecrire(session, essais, retenu, choisi)
    if retenu["pas"] == "questionner":
        sonder(session, retenu["qui"], retenu["cible"], retenu["detail"])
    if retenu["pas"] == "proposer" and choisi:
        _proposer(session, choisi)
    return {
        "tour": session.tour,
        "meilleur": choisi,
        "scores": scores,
        "direction": retenu["pas"],
        "gain": retenu["gain"],
    }


def _etat(session: Session) -> dict:
    """Options, gens, notes et vetos, via les requêtes nommées."""
    options = [ligne["option"] for ligne in executer(session, "options")]
    participants = [ligne["participant"] for ligne in executer(session, "participants")]
    notes: dict[str, dict[str, float]] = {personne: {} for personne in participants}
    for ligne in executer(session, "notes"):
        notes.setdefault(ligne["qui"], {})[ligne["option"]] = float(ligne["note"])
    vetos: dict[str, list[str]] = {personne: [] for personne in participants}
    for ligne in executer(session, "vetos"):
        vetos.setdefault(ligne["qui"], []).append(ligne["cible"])
    return {
        "options": options,
        "participants": participants,
        "notes": notes,
        "vetos": vetos,
    }


def _scores(etat: dict, regles: dict, blocage: bool) -> dict[str, dict]:
    scores = {}
    for option in etat["options"]:
        if blocage and any(option in cibles for cibles in etat["vetos"].values()):
            continue
        notes = {}
        vetos = {}
        for personne in etat["participants"]:
            connu = etat["notes"].get(personne, {}).get(option)
            notes[personne] = connu
            vetos[personne] = 1 if option in etat["vetos"].get(personne, []) else 0
        scores[option] = evaluer(notes, vetos, regles["veto_cout"])
    return scores


def _essais(session, etat, scores, choisi, regles, succes) -> list[dict]:
    essais = []
    actuel = _critere(scores, choisi, succes["critere"])
    if "conceder" in regles["pas"] and regles["mode_veto"] == "cout":
        for personne, cibles in etat["vetos"].items():
            for cible in cibles:
                hypothese = {
                    "options": etat["options"],
                    "participants": etat["participants"],
                    "notes": etat["notes"],
                    "vetos": {
                        pid: [item for item in liste if not (pid == personne and item == cible)]
                        for pid, liste in etat["vetos"].items()
                    },
                }
                apres = _scores(hypothese, regles, blocage=False)
                nouveau = meilleur(apres, succes["critere"])
                essais.append(
                    {
                        "pas": "conceder",
                        "gain": _critere(apres, nouveau, succes["critere"]) - actuel,
                        "qui": personne,
                        "cible": cible,
                        "detail": f"rendre négociable le veto de {personne} sur {cible}",
                    }
                )
    if "questionner" in regles["pas"] and choisi:
        for personne in etat["participants"]:
            if choisi in etat["notes"].get(personne, {}):
                continue
            if f"question-{personne}-{choisi}" in _questions(session):
                continue
            essais.append(
                {
                    "pas": "questionner",
                    "gain": 0.0,
                    "qui": personne,
                    "cible": choisi,
                    "detail": f"demander à {personne} une note sur {choisi}",
                }
            )
    if "proposer" in regles["pas"] and choisi:
        essais.append(
            {
                "pas": "proposer",
                "gain": 0.0,
                "cible": choisi,
                "detail": f"proposer {choisi}",
            }
        )
    if "tenir" in regles["pas"]:
        essais.append({"pas": "tenir", "gain": 0.0, "detail": "tenir le candidat courant"})
    return essais


def _choisir(essais, choisi, scores, succes) -> dict:
    progres = [essai for essai in essais if essai["pas"] == "conceder" and essai["gain"] > 0]
    if progres:
        progres.sort(key=lambda essai: -essai["gain"])
        return progres[0]
    questions = [essai for essai in essais if essai["pas"] == "questionner"]
    if questions:
        return questions[0]
    for essai in essais:
        if essai["pas"] == "proposer":
            return essai
    return {"pas": "tenir", "gain": 0.0, "detail": "tenir le candidat courant"}


def _ecrire(session: Session, essais: list[dict], retenu: dict, choisi: str | None) -> None:
    for index, essai in enumerate(essais):
        identifiant = f"chemin-{session.tour}-{index}"
        retenu_flag = essai["pas"] == retenu["pas"] and essai["detail"] == retenu["detail"]
        ajouter_noeud(
            session,
            "negociation",
            "Chemin",
            identifiant,
            {
                "pas": essai["pas"],
                "gain": float(essai["gain"]),
                "tour": session.tour,
                "detail": essai["detail"],
                "retenu": retenu_flag,
            },
        )
        if retenu_flag:
            direction = f"direction-{session.tour}"
            ajouter_noeud(
                session,
                "negociation",
                "Direction",
                direction,
                {
                    "pas": essai["pas"],
                    "gain": float(essai["gain"]),
                    "tour": session.tour,
                    "detail": essai["detail"],
                },
            )
            ajouter_lien(session, "negociation", "choisit", direction, identifiant)


def _proposer(session: Session, option: str) -> None:
    identifiant = f"proposition-{option}"
    try:
        ajouter_noeud(session, "negociation", "Proposition", identifiant, {"tour": session.tour})
    except ValueError:
        return
    ajouter_lien(session, "negociation", "retient", identifiant, option)


def _critere(scores: dict, identifiant: str | None, critere: str) -> float:
    if identifiant is None or identifiant not in scores:
        return 0.0
    return float(scores[identifiant][critere])


def _court(terme) -> str | None:
    if terme is None:
        return None
    texte = str(terme)
    if "/id/" in texte:
        return texte.split("/")[-1]
    return texte


def _questions(session: Session) -> set[str]:
    from rdflib import RDF

    from coeur.ns import NEGOCIATION

    return {
        _court(sujet)
        for sujet in session.faits.subjects(RDF.type, NEGOCIATION.Question)
    }
