"""Une question est un nœud. La réponse est un autre nœud, relié par ``repond``."""

from __future__ import annotations

from coeur.graphe import ajouter_lien, ajouter_noeud
from coeur.requetes import executer
from coeur.session import Session


def sonder(session: Session, qui: str, sur_quel_noeud: str, pourquoi: str) -> str:
    """Écrit la question. Ne invente pas la réponse."""
    identifiant = f"question-{qui}-{sur_quel_noeud}"
    ajouter_noeud(
        session,
        "negociation",
        "Question",
        identifiant,
        {"label": pourquoi, "pourquoi": pourquoi, "tour": session.tour},
    )
    ajouter_lien(session, "negociation", "pose", identifiant, qui)
    ajouter_lien(session, "negociation", "concerne", identifiant, sur_quel_noeud)
    return identifiant


def repondre(session: Session, question: str, qui: str, sur: str, note: float) -> str:
    """Écrit la réponse et la relie à la question et à l'option."""
    identifiant = f"reponse-{question}"
    ajouter_noeud(
        session,
        "negociation",
        "Reponse",
        identifiant,
        {"note": float(note), "tour": session.tour},
    )
    ajouter_lien(session, "negociation", "repond", identifiant, question)
    ajouter_lien(session, "negociation", "de", identifiant, qui)
    ajouter_lien(session, "negociation", "porteSur", identifiant, sur)
    return identifiant


def questions_ouvertes(session: Session) -> list[str]:
    """Identifiants des questions sans triplet ``repond``."""
    return [ligne["question"] for ligne in executer(session, "questions_sans_reponse")]
