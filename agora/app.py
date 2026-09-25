"""Interface Streamlit du MVP Agora.

Lancement : ``streamlit run agora/app.py``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ``streamlit run agora/app.py`` place le dossier du fichier sur le chemin,
# pas la racine du dépôt. Sans cet ajout, ``import agora`` échoue.
_RACINE = Path(__file__).resolve().parents[1]
if str(_RACINE) not in sys.path:
    sys.path.insert(0, str(_RACINE))

import pandas as pd
import streamlit as st

from agora.cli import GRAINE, executer, lister_scenarios
from agora.core.exploration import SEUIL_EXHAUSTIF
from agora.kr.charger import charger
from agora.kr.requetes import enumerer_candidats
from agora.scenarios import charger_scenario, preferences_figees
from agora.version import version_git

SEUIL_SAISIE = 12

RESUMES = {
    "vacances_3": "Trois personnes choisissent une destination, un logement et une activité.",
    "vacances_large": "Huit personnes et beaucoup de combinaisons.",
    "resto": "Trois personnes choisissent une cuisine, un quartier et un prix.",
    "weekend": "Trois personnes choisissent un jour, un lieu et un rythme.",
    "unanimite": "Cas limite : tout le monde est d'accord.",
    "conflit_total": "Cas limite : les envies s'opposent, sans veto.",
    "veto": "Cas limite : l'option préférée est refusée.",
    "egalite": "Cas limite : deux options se valent sur le point le plus faible.",
    "prefs_manquantes": "Cas limite : une grande partie des notes manque.",
}

NOMS_DIMENSIONS = {
    "destination": "destination",
    "logement": "logement",
    "activite": "activité",
    "transport": "transport",
    "saison": "saison",
    "duree": "durée",
    "cuisine": "cuisine",
    "quartier": "quartier",
    "prix": "prix",
    "jour": "jour",
    "lieu": "lieu",
    "rythme": "rythme",
    "option": "option",
}


def main() -> None:
    st.set_page_config(page_title="Agora", layout="wide")
    catalogue = lister_scenarios()
    labels = [item["label"] for item in catalogue]
    label = st.sidebar.selectbox("Scénario", labels, key="scenario")
    scenario_id = next(item["id"] for item in catalogue if item["label"] == label)
    scenario = charger_scenario(scenario_id)
    mode = st.sidebar.radio("Mode", ["Simuler", "Saisir"], key="mode_ui")

    st.title("Agora")
    st.write(
        "On cherche un compromis : le choix qui abîme le moins "
        "la personne la moins satisfaite."
    )
    st.write(RESUMES.get(scenario_id, ""))

    if mode == "Simuler":
        _section_simuler(scenario_id)
    else:
        _section_saisir(scenario, scenario_id)
    _section_script(scenario_id)

    if (
        st.session_state.get("resultat_scenario") == scenario_id
        and st.session_state.get("resultat")
    ):
        _afficher_resultat(st.session_state["resultat"], scenario)

    _barre_laterale(label, scenario_id)


def _section_simuler(scenario_id: str) -> None:
    st.subheader("Simuler")
    st.write(
        "Des profils automatiques négocient à la place du groupe. "
        f"La graine du tirage est {GRAINE} : le même scénario redonne le même résultat."
    )
    if st.button("Lancer la négociation", type="primary", key="lancer"):
        with st.spinner("Négociation en cours…"):
            resultat = executer(scenario_id, simuler=True, seed=GRAINE)
        _memoriser(scenario_id, resultat, script=False)


def _section_saisir(scenario: dict, scenario_id: str) -> None:
    st.subheader("Saisir")
    groupes = _valeurs_par_dimension(scenario)
    nombre = sum(len(options) for options in groupes.values())
    if nombre > SEUIL_SAISIE:
        st.info(
            "Trop d'options pour les noter une par une. "
            "Lancez la simulation, ou collez un JSON plus bas."
        )
        return

    st.write(
        "Notez de -10 (à éviter) à 10 (idéal). "
        "Laissez vide si la personne ne se prononce pas : "
        "un vide n'est pas un zéro. Cochez veto si l'option est inacceptable."
    )
    figées = preferences_figees(scenario) or {"notes": {}, "veto": {}}
    saisies: list[tuple[str, str, float | None, bool]] = []
    for personne in scenario.get("participants") or []:
        pid = personne["id"]
        st.markdown(f"**{personne.get('label') or pid}**")
        notes_personne = (figées.get("notes") or {}).get(pid) or {}
        veto_personne = (figées.get("veto") or {}).get(pid) or []
        for dimension, options in groupes.items():
            st.caption(_nom_dimension(dimension))
            for option in options:
                oid = option["id"]
                col_note, col_veto = st.columns([3, 1])
                initiale = notes_personne.get(oid)
                with col_note:
                    valeur = st.number_input(
                        option.get("label") or oid,
                        min_value=-10,
                        max_value=10,
                        value=None if initiale is None else int(initiale),
                        step=1,
                        key=f"note-{scenario_id}-{pid}-{oid}",
                    )
                with col_veto:
                    coche = st.checkbox(
                        "Veto",
                        value=oid in veto_personne,
                        key=f"veto-{scenario_id}-{pid}-{oid}",
                    )
                saisies.append((pid, oid, valeur, coche))

    if st.button("Calculer le compromis", type="primary", key="calculer"):
        notes: dict[str, dict] = {}
        veto: dict[str, list] = {}
        for pid, oid, valeur, coche in saisies:
            if valeur is not None:
                notes.setdefault(pid, {})[oid] = int(valeur)
            if coche:
                veto.setdefault(pid, []).append(oid)
        resultat = executer(
            scenario_id,
            simuler=False,
            seed=GRAINE,
            preferences={"notes": notes, "veto": veto},
            fusionner=False,
        )
        _memoriser(scenario_id, resultat, script=False)


def _section_script(scenario_id: str) -> None:
    st.subheader("Pour un script")
    st.write("Le même calcul, depuis un terminal.")
    st.code(
        "\n".join(
            [
                "python -m agora.cli scenarios",
                f"python -m agora.cli run {scenario_id} --simuler --seed {GRAINE}",
                f"python -m agora.cli run {scenario_id} --prefs prefs.json",
            ]
        ),
        language="bash",
    )
    st.write('Collez un JSON `{"notes": {...}, "veto": {...}}`.')
    texte = st.text_area(
        "JSON de préférences",
        height=160,
        placeholder='{"notes": {"p1": {"favori": 8}}, "veto": {"p1": ["favori"]}}',
        key=f"json-{scenario_id}",
    )
    if st.button("Calculer depuis le JSON", key="calculer_json"):
        if not texte.strip():
            st.error("Collez un JSON de préférences.")
            return
        try:
            prefs = json.loads(texte)
        except json.JSONDecodeError:
            st.error("Ce JSON n'est pas lisible.")
            return
        if not isinstance(prefs, dict):
            st.error("Le JSON doit être un objet avec notes et veto.")
            return
        try:
            resultat = executer(
                scenario_id,
                simuler=False,
                seed=GRAINE,
                preferences=prefs,
                fusionner=True,
            )
        except (OSError, ValueError, TypeError) as exc:
            st.error(str(exc))
            return
        _memoriser(scenario_id, resultat, script=True)

    if (
        st.session_state.get("resultat_scenario") == scenario_id
        and st.session_state.get("origine") == "script"
        and st.session_state.get("resultat")
    ):
        st.json(st.session_state["resultat"])


def _afficher_resultat(resultat: dict, scenario: dict) -> None:
    st.subheader("Résultat")
    st.write(_phrase(resultat, scenario))
    meilleur = resultat.get("meilleur") or {}
    if meilleur.get("id"):
        st.caption(f"Référence : {meilleur['id']}")

    st.markdown("**Classement**")
    st.dataframe(_tableau_classement(resultat.get("classement") or []), hide_index=True)

    st.markdown("**Historique des rounds**")
    historique = resultat.get("historique") or []
    if historique:
        st.dataframe(_tableau_historique(historique), hide_index=True)
    else:
        st.caption("Pas encore de rounds successifs.")

    _afficher_progression(resultat)


def _afficher_progression(resultat: dict) -> None:
    st.subheader("Progression")
    historique = resultat.get("historique") or []
    if len(historique) < 2:
        chiffres = _chiffres(resultat)
        colonnes = st.columns(len(chiffres))
        for colonne, (titre, valeur) in zip(colonnes, chiffres.items()):
            colonne.metric(titre, _formater_nombre(valeur))
        st.info("un seul round : pas encore de courbe")
        return

    series = (
        ("least_misery", "Satisfaction min"),
        ("moyenne", "Satisfaction moyenne"),
        ("penalite", "Pénalité / veto"),
        ("dispersion", "Dispersion"),
        ("entropie", "Entropie H_round"),
    )
    for cle, titre in series:
        st.markdown(f"**{titre}**")
        st.line_chart(_courbe(historique, cle, titre))


def _phrase(resultat: dict, scenario: dict) -> str:
    accord = resultat.get("accord") or {}
    textes = [
        clause["texte"]
        for clause in (accord.get("clauses") or [])
        if clause.get("texte")
    ]
    if textes:
        return "Compromis : " + ", ".join(textes) + "."
    meilleur = resultat.get("meilleur") or {}
    choix = meilleur.get("choix") or {}
    libelles = {
        noeud["id"]: noeud.get("label") or noeud["id"]
        for noeud in scenario.get("noeuds") or []
    }
    if choix:
        morceaux = [
            f"{_nom_dimension(dimension)} = {libelles.get(valeur, valeur)}"
            for dimension, valeur in choix.items()
        ]
        return "Compromis : " + ", ".join(morceaux) + "."
    if meilleur.get("id"):
        return f"Compromis retenu : {meilleur['id']}."
    return "Aucun compromis trouvé."


def _tableau_classement(classement: list[dict]) -> pd.DataFrame:
    colonnes = ["candidat", "least misery", "moyenne", "pénalité", "dispersion"]
    lignes = [
        {
            "candidat": candidat.get("id"),
            "least misery": candidat.get("least_misery"),
            "moyenne": candidat.get("moyenne"),
            "pénalité": candidat.get("penalite"),
            "dispersion": candidat.get("dispersion"),
        }
        for candidat in classement[:15]
    ]
    return pd.DataFrame(lignes, columns=colonnes)


def _tableau_historique(historique: list[dict]) -> pd.DataFrame:
    colonnes = [
        "round",
        "candidat",
        "least misery",
        "moyenne",
        "pénalité",
        "dispersion",
        "entropie",
    ]
    lignes = [
        {
            "round": ligne.get("round"),
            "candidat": ligne.get("meilleur_id"),
            "least misery": ligne.get("least_misery"),
            "moyenne": ligne.get("moyenne"),
            "pénalité": ligne.get("penalite"),
            "dispersion": ligne.get("dispersion"),
            "entropie": ligne.get("entropie", ligne.get("H_round")),
        }
        for ligne in historique
    ]
    return pd.DataFrame(lignes, columns=colonnes)


def _courbe(historique: list[dict], cle: str, titre: str) -> pd.DataFrame:
    valeurs = []
    for ligne in historique:
        if cle == "entropie":
            valeurs.append(ligne.get("entropie", ligne.get("H_round")))
        else:
            valeurs.append(ligne.get(cle))
    return pd.DataFrame(
        {"round": [ligne.get("round") for ligne in historique], titre: valeurs}
    ).set_index("round")


def _chiffres(resultat: dict) -> dict[str, float | None]:
    historique = resultat.get("historique") or []
    if len(historique) == 1:
        source = historique[0]
        entropie = source.get("entropie", source.get("H_round"))
    else:
        source = resultat.get("metriques") or {}
        entropie = source.get("H_round", source.get("entropie"))
    meilleur = resultat.get("meilleur") or {}
    return {
        "Satisfaction min": source.get("least_misery", meilleur.get("least_misery")),
        "Satisfaction moyenne": source.get("moyenne", meilleur.get("moyenne")),
        "Pénalité": source.get("penalite", meilleur.get("penalite")),
        "Dispersion": source.get("dispersion", meilleur.get("dispersion")),
        "Entropie H_round": entropie,
    }


def _formater_nombre(valeur) -> str:
    if valeur is None:
        return "—"
    return f"{float(valeur):.2f}"


def _memoriser(scenario_id: str, resultat: dict, *, script: bool) -> None:
    st.session_state["resultat"] = resultat
    st.session_state["resultat_scenario"] = scenario_id
    st.session_state["origine"] = "script" if script else "ui"


def _barre_laterale(label: str, scenario_id: str) -> None:
    mode = None
    if st.session_state.get("resultat_scenario") == scenario_id:
        mode = (st.session_state.get("resultat") or {}).get("mode")
    if mode not in {"exhaustif", "genetique"}:
        mode = _mode_exploration(scenario_id)
    st.sidebar.divider()
    st.sidebar.caption("Version git")
    st.sidebar.write(version_git())
    st.sidebar.caption("Scénario")
    st.sidebar.write(label)
    st.sidebar.caption("Exploration")
    st.sidebar.write("génétique" if mode == "genetique" else "exhaustif")


@st.cache_data(show_spinner=False)
def _mode_exploration(nom: str) -> str:
    scenario = charger_scenario(nom)
    graphe = charger(scenario)
    nombre = len(enumerer_candidats(graphe, limite=SEUIL_EXHAUSTIF + 1))
    if nombre <= SEUIL_EXHAUSTIF:
        return "exhaustif"
    return "genetique"


def _valeurs_par_dimension(scenario: dict) -> dict[str, list[dict]]:
    groupes = {dimension: [] for dimension in scenario.get("dimensions") or []}
    for noeud in scenario.get("noeuds") or []:
        if noeud.get("type") in groupes:
            groupes[noeud["type"]].append(noeud)
    return groupes


def _nom_dimension(dimension: str) -> str:
    return NOMS_DIMENSIONS.get(dimension, dimension)


main()
