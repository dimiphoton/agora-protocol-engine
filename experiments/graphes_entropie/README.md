# Expérience D — Graphes et entropie

## Hypothèse

On peut **résumer mathématiquement** une situation de désaccord : graphe de
positions + entropie de Shannon par dimension. L'entropie n'est pas le score
de qualité d'une solution (ça c'est least misery) ; c'est le **compteur de
processus** (échanges 115, 189) : incertitude, dispersion, où sonder.

Le progrès n'est **pas monotone** : l'entropie peut remonter (nouveau grief).
Ici on mesure un instantané + un petit choc (P2 révèle un veto festivals).

## Lancer

```bash
cd experiments/graphes_entropie
python proto.py
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `H(dimension)` | Entropie de la distribution des votes sur une dimension. Haute = désaccord / indécision. |
| `H_cons` | Somme pondérée. KPI central du brainstorming. |
| `question_max_gain` | Dimension qui, si clarifiée, réduirait le plus H_cons (élicitation active). |
| `distance_ij` | Désaccord moyen |note_i − note_j|. Graphe de positions. |
