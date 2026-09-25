# Expérience B — Guerre des mots

## Hypothèse

Chaque parti arrive avec **son vocabulaire**. Le désaccord n'est pas (seulement)
une différence de préférences : c'est une divergence d'ontologies privées
(échange 213). L'alignement / traduction / mesure de divergence est un
préalable à tout scoring.

Le brainstorming nomme ça la « guerre des mots » et propose une **Bourse de
Neutralisation Sémantique** : un terme-pont qui ne viole ni l'une ni l'autre
philosophie, plutôt qu'une fusion forcée.

## Ce que le brainstorming dit

- Jamais une seule ontologie au départ : privées → négociation → consensus.
- L'IA ne juge pas quelle étiquette est « vraie » (terroriste vs combattant).
- Pour le MVP vacances, la guerre des mots existe déjà à petite échelle
  (`camping` = « liberté » vs « précarité »).

## Lancer

```bash
cd experiments/guerre_des_mots
python proto.py
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `divergence_lexicale` | 1 − Jaccard des termes bruts. Haute = les gens ne parlent pas la même langue. |
| `divergence_alignee` | Jaccard après table de traduction. Si elle chute, le conflit était surtout lexical. |
| `taux_neutralisation` | Part des paires conflictuelles pour lesquelles un terme-pont existe. |
| `residual_wars` | Paires encore irréductibles (pas de pont). C'est le vrai conflit politique. |
| `delta_divergence` | Gain de l'alignement. C'est l'utilité du lexicographe. |
