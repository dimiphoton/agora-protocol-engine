"""Règles de négociation, écrites dans le graphe."""

from __future__ import annotations

from coeur.graphe import ajouter_noeud, poser_attribut
from coeur.requetes import executer
from coeur.session import Session

PAS = ("proposer", "conceder", "questionner", "tenir")


def definir_regles(
    session: Session,
    pas: tuple[str, ...] = PAS,
    mode_veto: str = "cout",
    veto_cout: float = 100.0,
) -> None:
    """Enregistre les pas permis et le traitement du veto (``cout`` ou ``blocage``)."""
    if mode_veto not in ("cout", "blocage"):
        raise ValueError("mode_veto doit être cout ou blocage")
    for nom in pas:
        if nom not in PAS:
            raise ValueError(f"pas inconnu : {nom}")
    ajouter_noeud(session, "negociation", "Reglage", "reglage")
    poser_attribut(session, "reglage", "modeVeto", mode_veto)
    poser_attribut(session, "reglage", "vetoCout", float(veto_cout))
    for nom in pas:
        poser_attribut(session, "reglage", "autorise", nom)


def lire_regles(session: Session) -> dict:
    """Relit le réglage par SPARQL."""
    lignes = executer(session, "reglage")
    if not lignes:
        raise ValueError("aucune règle définie")
    pas = []
    for ligne in lignes:
        if ligne.get("pas") and ligne["pas"] not in pas:
            pas.append(ligne["pas"])
    premiere = lignes[0]
    return {
        "pas": pas,
        "mode_veto": premiere.get("modeVeto") or "cout",
        "veto_cout": float(premiere["vetoCout"]) if premiere.get("vetoCout") else 100.0,
    }
