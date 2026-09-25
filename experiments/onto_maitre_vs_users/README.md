# Expérience C — Branches maître vs utilisateurs

## Hypothèse

Deux régimes d'extension de l'arbre :

1. **Maître** : un gardien (le « bibliothécaire » du protocole, ou le
   concepteur du MVP) pose les branches. Cohérence haute, expressivité basse.
2. **Utilisateurs** : chacun ajoute des concepts / relations (Wikipédia,
   échange 14). Expressivité haute, cohérence qui se dégrade (contradictions,
   cycles, capture idéologique).

Le brainstorming tranche pour le MVP : ontologie **contrôlée** d'abord,
collaborative ensuite, avec un **score de confiance** par relation.

## Lancer

```bash
cd experiments/onto_maitre_vs_users
python proto.py
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `coherence` | 1 − (contradictions + cycles + orphelins) / relations. 1.0 = graphe sain. |
| `expressivite` | Part des énoncés utilisateurs représentables. |
| `capture` | Part des nouveaux nœuds proposés par un seul participant. Risque wiki. |
| `confiance_moyenne` | Moyenne des votes d'éditeurs sur les relations (idée échange 14). |
