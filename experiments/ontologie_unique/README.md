# Expérience A — Ontologie unique partagée

## Hypothèse

Une **seule ontologie de domaine**, écrite comme graphe de concepts communs, suffit
à encoder le sens d'un petit conflit (MVP vacances, échange 8) : les désaccords
ne portent pas sur les mots, ils portent sur des **préférences** déjà mappées
vers les mêmes nœuds (`voile`, `camping`, `accès_mer`, …).

C'est le modèle "tableur intelligent" : l'ontologie infère (`voile` requiert
`accès_mer` ; Auvergne n'a pas `accès_mer`) au lieu de tout demander.

## Ce que le brainstorming dit

- L'ontologie ne doit pas être décorative : elle doit filtrer, inférer,
  reformuler (`ontologie-semantique.md`).
- Pour le MVP : dictionnaires Python, pas RDF/OWL.
- L'échange 213 dit qu'il n'y a **jamais une seule ontologie** dans un conflit
  politique. Cette expérience teste le cas *simple* (vacances) où l'unicité
  est plausible.

## Lancer

```bash
cd experiments/ontologie_unique
python proto.py
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `taux_mapping` | Part des énoncés utilisateurs rattachés à un concept commun. 1.0 = plus de jargon orphelin. |
| `inferences` | Contraintes déduites (pas déclarées). Plus c'est haut, plus l'ontologie "travaille". |
| `conflits_conceptuels` | Deux participants s'opposent sur le **même** concept. C'est un vrai désaccord, pas une guerre de mots. |
| `orphelin` | Mot non mappé : coût cognitif futur, ou besoin d'étendre l'arbre. |
| `options_valides` | Combinaisons qui survivent aux inférences dures (`requiert` / `incompatible`). |
