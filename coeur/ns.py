"""Espaces de noms du cœur. Aucun vocabulaire de domaine ici."""

from rdflib import Namespace

DOMAINE = Namespace("https://agora.local/domaine#")
NEGOCIATION = Namespace("https://agora.local/negociation#")

PREFIXES = {
    "domaine": DOMAINE,
    "negociation": NEGOCIATION,
}


def uri_noeud(ontologie: str, identifiant: str) -> str:
    """URI stable d'une instance : ``https://agora.local/id/{ontologie}/{id}``."""
    return f"https://agora.local/id/{ontologie}/{identifiant}"
