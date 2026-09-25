"""Seule porte d'écriture : ajouter un nœud ou un lien déclaré."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Literal, RDF, RDFS, URIRef

from coeur.ns import PREFIXES, uri_noeud
from coeur.session import Session

PROPRIETES_STANDARD = {RDFS.label}


def ajouter_noeud(
    session: Session,
    ontologie: str,
    type_nom: str,
    identifiant: str,
    attributs: dict | None = None,
) -> URIRef:
    """Ajoute une instance. La classe doit être déclarée dans l'ontologie."""
    classe = _classe(session, ontologie, type_nom)
    noeud = URIRef(uri_noeud(ontologie, identifiant))
    if (noeud, RDF.type, classe) in session.faits:
        raise ValueError(f"nœud déjà présent : {identifiant}")
    session.faits.add((noeud, RDF.type, classe))
    for cle, valeur in (attributs or {}).items():
        session.faits.add((noeud, _propriete_attribut(session, cle), _litteral(valeur)))
    return noeud


def ajouter_lien(
    session: Session,
    ontologie: str,
    relation: str,
    source: str,
    cible: str,
) -> None:
    """Ajoute un triplet. La relation doit être déclarée, le domaine et la portée aussi."""
    prop = _relation(session, ontologie, relation)
    source_uri = _trouver(session, source)
    cible_uri = _trouver(session, cible)
    _verifier_portee(session, ontologie, prop, source_uri, RDFS.domain)
    _verifier_portee(session, ontologie, prop, cible_uri, RDFS.range)
    session.faits.add((source_uri, prop, cible_uri))


def poser_attribut(session: Session, identifiant: str, cle: str, valeur) -> None:
    """Pose un littéral sur un nœud déjà créé. ``autorise`` peut être répété."""
    noeud = _trouver(session, identifiant)
    prop = _propriete_attribut(session, cle)
    if cle != "autorise":
        session.faits.remove((noeud, prop, None))
    session.faits.add((noeud, prop, _litteral(valeur)))


def importer(session: Session, chemin: str | Path) -> None:
    """Lit un Turtle d'instances en passant par ``ajouter_noeud`` et ``ajouter_lien``."""
    brut = Graph()
    brut.parse(Path(chemin), format="turtle")
    for sujet, objet in brut.subject_objects(RDF.type):
        ontologie, type_nom = _ontologie_de_classe(session, objet)
        label = brut.value(sujet, RDFS.label)
        attributs = {"label": str(label)} if label is not None else None
        ajouter_noeud(session, ontologie, type_nom, _identifiant(sujet), attributs)
    for sujet, prop, objet in brut:
        if prop in (RDF.type, RDFS.label) or isinstance(objet, Literal):
            continue
        ontologie, relation = _ontologie_de_propriete(session, prop)
        ajouter_lien(
            session,
            ontologie,
            relation,
            _identifiant(sujet),
            _identifiant(objet),
        )


def _classe(session: Session, ontologie: str, type_nom: str) -> URIRef:
    graphe = _ontologie(session, ontologie)
    classe = PREFIXES[ontologie][type_nom]
    if (classe, RDF.type, RDFS.Class) not in graphe:
        raise ValueError(f"classe non déclarée : {ontologie}:{type_nom}")
    return classe


def _relation(session: Session, ontologie: str, relation: str) -> URIRef:
    graphe = _ontologie(session, ontologie)
    prop = PREFIXES[ontologie][relation]
    if (prop, RDF.type, RDF.Property) not in graphe:
        raise ValueError(f"relation non déclarée : {ontologie}:{relation}")
    return prop


def _propriete_attribut(session: Session, cle: str) -> URIRef:
    if cle == "label":
        return RDFS.label
    for ontologie, espace in PREFIXES.items():
        prop = espace[cle]
        if ontologie in session.ontologies and (prop, RDF.type, RDF.Property) in session.ontologies[ontologie]:
            return prop
    raise ValueError(f"attribut non déclaré : {cle}")


def _verifier_portee(session: Session, ontologie: str, prop: URIRef, noeud: URIRef, role: URIRef) -> None:
    attendu = session.ontologies[ontologie].value(prop, role)
    if attendu is None:
        return
    if (noeud, RDF.type, attendu) not in session.faits:
        raise ValueError(f"{noeud} n'est pas un {attendu}")


def _trouver(session: Session, identifiant: str) -> URIRef:
    for ontologie in session.ontologies:
        noeud = URIRef(uri_noeud(ontologie, identifiant))
        if (noeud, RDF.type, None) in session.faits:
            return noeud
    raise ValueError(f"nœud inconnu : {identifiant}")


def _ontologie(session: Session, nom: str) -> Graph:
    if nom not in session.ontologies:
        raise ValueError(f"ontologie non déclarée : {nom}")
    return session.ontologies[nom]


def _ontologie_de_classe(session: Session, classe: URIRef) -> tuple[str, str]:
    for nom, espace in PREFIXES.items():
        if str(classe).startswith(str(espace)):
            return nom, str(classe)[len(str(espace)) :]
    raise ValueError(f"classe hors ontologie : {classe}")


def _ontologie_de_propriete(session: Session, prop: URIRef) -> tuple[str, str]:
    for nom, espace in PREFIXES.items():
        if str(prop).startswith(str(espace)):
            return nom, str(prop)[len(str(espace)) :]
    raise ValueError(f"relation hors ontologie : {prop}")


def _identifiant(noeud: URIRef) -> str:
    texte = str(noeud)
    marqueur = "/id/"
    if marqueur not in texte:
        raise ValueError(f"URI d'instance illisible : {noeud}")
    return texte.split("/")[-1]


def _litteral(valeur):
    if isinstance(valeur, bool):
        return Literal(valeur)
    if isinstance(valeur, (int, float)):
        return Literal(valeur)
    return Literal(str(valeur))
