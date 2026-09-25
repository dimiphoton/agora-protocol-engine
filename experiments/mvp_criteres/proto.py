"""Cadre de mesure + classement ordonné des MVPs.

Les chiffres A–F sont recopiés des runs du 2026-09-25 (bots, 3 personnes,
scénario vacances / copropriété). La grille est volontairement lisible :
pondérations explicites, pas de modèle caché.
"""

from __future__ import annotations

import pandas as pd

# Preuves expérimentales (runs A–F)
RUNS = {
    "A_taux_mapping": 0.929,
    "A_n_inferences": 13.0,
    "A_taux_filtrage": 0.083,
    "B_div_lexicale": 1.000,
    "B_delta_align": 0.426,
    "C_maitre_coh": 0.889,
    "C_maitre_expr": 0.273,
    "C_hybride_coh": 0.889,
    "C_hybride_expr": 0.818,
    "D_H_cons": 1.038,
    "D_delta_choc": 0.057,
    "E_least_misery": 8.0,
    "E_gap": 0.0,
    "E_palier_gen": 8.0,
    "F_vac_rounds": 3.0,
    "F_vac_vetos": 1.0,
    "F_copro_vetos": 2.0,
    "F_copro_anonymat": 1.0,
}

# Critères : 0–5. Commentés pour rester contestables.
CRITERES = [
    "utilite",          # un accord lisible, least misery, sens (ontologie)
    "efficacite",       # peu de rounds / gens, ΔH utile
    "cout_cognitif",    # inverse : 5 = facile à expliquer / peu de questions
    "temps_consensus",  # 5 = rapide sur un cas jouet
    "robustesse_veto",  # 5 = un veto n'annule pas l'espace
    "prouvable_console",
    "risque_politique", # 5 = faible risque (vacances) ; 0 = paix
    "indep_blockchain",
]


def score_mvp(nom: str, notes: dict[str, float], pourquoi: str) -> dict:
    row = {"mvp": nom, **notes, "pourquoi": pourquoi}
    row["total"] = sum(notes[c] for c in CRITERES) / len(CRITERES)
    return row


def tableau() -> pd.DataFrame:
    rows = [
        score_mvp(
            "0_vacances_least_misery",
            {
                "utilite": 4, "efficacite": 5, "cout_cognitif": 5,
                "temps_consensus": 5, "robustesse_veto": 2,
                "prouvable_console": 5, "risque_politique": 5,
                "indep_blockchain": 5,
            },
            "échange 4 ; E confirme (Bretagne, Hôtel, Voile) LM=8, gap AG=0. "
            "Veto encore naïf (d'où 2).",
        ),
        score_mvp(
            "1_ontologie_domaine",
            {
                "utilite": 5, "efficacite": 4, "cout_cognitif": 3,
                "temps_consensus": 4, "robustesse_veto": 3,
                "prouvable_console": 5, "risque_politique": 5,
                "indep_blockchain": 5,
            },
            f"A : mapping {RUNS['A_taux_mapping']}, {int(RUNS['A_n_inferences'])} inférences, "
            f"filtrage {RUNS['A_taux_filtrage']:.0%} (Auvergne+voile). "
            "Sans ça le MVP 0 est un tableur.",
        ),
        score_mvp(
            "1b_H_cons_graphe",
            {
                "utilite": 3, "efficacite": 5, "cout_cognitif": 3,
                "temps_consensus": 4, "robustesse_veto": 3,
                "prouvable_console": 5, "risque_politique": 5,
                "indep_blockchain": 5,
            },
            f"D : H_cons={RUNS['D_H_cons']} bits, choc veto ΔH=+{RUNS['D_delta_choc']}. "
            "Tableau de bord, pas le moteur. Coût cognitif : expliquer l'entropie.",
        ),
        score_mvp(
            "2_regles_yaml",
            {
                "utilite": 4, "efficacite": 4, "cout_cognitif": 4,
                "temps_consensus": 4, "robustesse_veto": 5,
                "prouvable_console": 5, "risque_politique": 5,
                "indep_blockchain": 5,
            },
            f"F vacances : {int(RUNS['F_vac_rounds'])} rounds, "
            f"{int(RUNS['F_vac_vetos'])} veto payé puis concession, retour LM=+3. "
            "Veto=prix, pas mur.",
        ),
        score_mvp(
            "3_copropriete_travaux",
            {
                "utilite": 4, "efficacite": 3, "cout_cognitif": 3,
                "temps_consensus": 3, "robustesse_veto": 5,
                "prouvable_console": 4, "risque_politique": 4,
                "indep_blockchain": 5,
            },
            f"F copro : anonymat, {int(RUNS['F_copro_vetos'])} vetos, 2 concessions. "
            "Gens qui ne s'apprécient pas. Test réel de B (labels).",
        ),
        score_mvp(
            "4_budget_collectif",
            {
                "utilite": 4, "efficacite": 3, "cout_cognitif": 2,
                "temps_consensus": 2, "robustesse_veto": 4,
                "prouvable_console": 3, "risque_politique": 3,
                "indep_blockchain": 5,
            },
            "Backlog brut. Plus de votants → AG (E) devient utile. Pas prototyé ici.",
        ),
        score_mvp(
            "5_ontologie_collaborative",
            {
                "utilite": 3, "efficacite": 2, "cout_cognitif": 2,
                "temps_consensus": 2, "robustesse_veto": 3,
                "prouvable_console": 3, "risque_politique": 3,
                "indep_blockchain": 5,
            },
            "C : users expr=0.909 mais cycle+contradiction ; "
            f"hybride confiance coh={RUNS['C_hybride_coh']} expr={RUNS['C_hybride_expr']}. "
            "Après un tronc stable.",
        ),
        score_mvp(
            "6_guerre_des_mots",
            {
                "utilite": 5, "efficacite": 3, "cout_cognitif": 2,
                "temps_consensus": 2, "robustesse_veto": 3,
                "prouvable_console": 4, "risque_politique": 2,
                "indep_blockchain": 5,
            },
            f"B : Δ divergence={RUNS['B_delta_align']} (lexicale {RUNS['B_div_lexicale']} "
            "→ alignée 0.57). Vital dès l'identité ; trop tôt comme premier écran.",
        ),
        score_mvp(
            "9_paix_onchain",
            {
                "utilite": 5, "efficacite": 1, "cout_cognitif": 0,
                "temps_consensus": 0, "robustesse_veto": 2,
                "prouvable_console": 0, "risque_politique": 0,
                "indep_blockchain": 0,
            },
            "Vision. Cold start. Calcul on-chain prohibitif (échange 104). Pas maintenant.",
        ),
    ]
    df = pd.DataFrame(rows).sort_values("total", ascending=False)
    df["rang"] = range(1, len(df) + 1)
    return df[["rang", "mvp", "total", *CRITERES, "pourquoi"]]


def main() -> None:
    df = tableau()
    print("=== Cadre de mesure — classement MVP ===")
    print("Pondération : moyenne simple des 8 critères (0–5).")
    print(df.drop(columns=["pourquoi"]).round(2).to_string(index=False))
    print("\nJustifications :")
    for _, row in df.iterrows():
        print(f"  {int(row.rang)}. {row.mvp}  total={row.total:.2f}")
        print(f"     {row.pourquoi}")
    print("\nSéquence de code recommandée : 0 → 1 → 1b → 2 → 3.")
    print("Ne pas commencer par 6, 5 ou 9 malgré leur charge symbolique.")
    print("\nPreuves A–F recopiées :")
    for k, v in RUNS.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
