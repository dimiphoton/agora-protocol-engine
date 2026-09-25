"""Boucle multi-rounds au-dessus de ``tourner`` (un round, historique vide)."""

from __future__ import annotations

from agora.core.chemins import essayer_chemins, lire_chemins
from agora.core.moteur import tourner
from agora.kr.charger import charger
from agora.kr.negociation import (
    cloturer_accord,
    enregistrer_round,
    enregistrer_veto,
    lire_accord,
    poser_negociation,
)
from agora.simulateurs.bruite import voter as voter_bruite
from agora.simulateurs.cooperatif import voter as voter_cooperatif
from agora.simulateurs.incomplet import voter as voter_incomplet
from agora.simulateurs.veto_prone import voter as voter_veto

PROFILS = {
    "cooperatif": voter_cooperatif,
    "veto_prone": voter_veto,
    "incomplet": voter_incomplet,
    "bruite": voter_bruite,
}

# Même meilleur pendant autant de rounds : on s'arrête.
TOURS_STABLE = 3


def jouer(
    scenario: dict,
    profils: dict[str, str],
    seed: int = 0,
    max_rounds: int = 8,
) -> dict:
    """Joue une négociation simulée et lit l'accord sur le graphe.

    À chaque round, une partie des participants seulement met à jour
    son vote (round robin, au moins une personne). Les autres gardent
    leurs préférences. On s'arrête si le même ``meilleur_id`` tient
    trois rounds de suite, ou au plafond ``max_rounds`` (8 par défaut).
    """
    graphe = charger(scenario)
    poser_negociation(scenario, graphe)
    personnes = {
        participant["id"]: participant
        for participant in scenario["participants"]
    }
    identifiants = list(personnes)
    notes: dict[str, dict] = {}
    veto: dict[str, list] = {}
    historique: list[dict] = []
    dernier = None

    for numero in range(1, max_rounds + 1):
        propositions = []
        notes_recues = 0
        for pid in participants_du_round(identifiants, numero):
            if pid not in profils:
                raise ValueError(f"profil manquant pour {pid}")
            nom = profils[pid]
            if nom not in PROFILS:
                raise ValueError(f"profil inconnu : {nom}")
            vote = PROFILS[nom](personnes[pid], scenario, seed)
            notes[pid] = dict(vote["notes"])
            veto[pid] = list(vote["veto"])
            notes_recues += len(notes[pid])
            propositions.append(
                {
                    "participant_id": pid,
                    "notes": dict(notes[pid]),
                    "veto": list(veto[pid]),
                }
            )

        resultat = tourner(scenario, {"notes": notes, "veto": veto}, seed=seed)
        dernier = resultat
        meilleur = resultat["meilleur"]
        meilleur_id = meilleur["id"] if meilleur else None
        enregistrer_round(graphe, numero, meilleur_id, propositions)
        for proposition in propositions:
            for cible in proposition["veto"]:
                enregistrer_veto(
                    graphe,
                    proposition["participant_id"],
                    cible,
                    numero,
                )
        metriques = resultat["metriques"]
        historique.append(
            {
                "round": numero,
                "meilleur_id": meilleur_id,
                "least_misery": metriques["least_misery"],
                "moyenne": metriques["moyenne"],
                "penalite": metriques["penalite"],
                "dispersion": metriques["dispersion"],
                "entropie": metriques["H_round"],
                "taux_manquant": metriques["taux_manquant"],
                "notes_recues": notes_recues,
            }
        )
        bilan = essayer_chemins(
            graphe,
            {"notes": notes, "veto": veto},
            numero=numero,
            seed=seed,
        )
        historique[-1]["direction"] = bilan["retenu"]
        if _meme_meilleur(historique):
            break

    meilleur = dernier["meilleur"] if dernier else None
    cloturer_accord(graphe, meilleur)
    return {
        "classement": dernier["classement"] if dernier else [],
        "meilleur": meilleur,
        "historique": historique,
        "metriques": dernier["metriques"] if dernier else {},
        "accord": lire_accord(graphe),
        "graphe": graphe,
        "mode": dernier["mode"] if dernier else None,
        "preferences": {"notes": notes, "veto": veto},
        "chemins": lire_chemins(graphe),
    }


def participants_du_round(identifiants: list[str], numero: int) -> list[str]:
    """Partie tournante du groupe. Au moins une personne.

    Taille ``max(1, n // 2)`` : une personne sur deux, par blocs qui
    se relaient. À une personne près, elle vote à chaque round. À
    plusieurs, le bloc ne couvre pas tout le groupe.
    """
    n = len(identifiants)
    if n == 0:
        return []
    taille = max(1, n // 2)
    if n > 1 and taille >= n:
        taille = n - 1
    depart = ((int(numero) - 1) * taille) % n
    return [identifiants[(depart + i) % n] for i in range(taille)]


def _meme_meilleur(historique: list[dict], tours: int = TOURS_STABLE) -> bool:
    if len(historique) < tours:
        return False
    derniers = [ligne["meilleur_id"] for ligne in historique[-tours:]]
    return derniers[0] == derniers[1] == derniers[2]
