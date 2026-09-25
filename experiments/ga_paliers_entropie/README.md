# Expérience E — Algorithme génétique et paliers d'entropie

## Hypothèse

Quand l'espace n'est plus enumerable (échange 5), un AG explore des package
deals. On s'arrête sur un **palier d'entropie** (échange 189) : H_cons et
fitness du meilleur ne bougent plus pendant `patience` générations.

Ce n'est pas une descente de gradient (échange 3) : espace discret.
Fitness = least misery, veto = pénalité massive (échange 7), pas un mur.

## Lancer

```bash
cd experiments/ga_paliers_entropie
python proto.py
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `best_least_misery` | min(scores) du meilleur génome. Plus haut = moins de frustration max. |
| `H_pop` | Entropie de la population (diversité des génomes). Chute = convergence. |
| `generation_palier` | Génération où le critère d'arrêt palier s'est déclenché. |
| `gap_vs_exhaustif` | Écart à l'optimum connu (espace encore petit ici, pour vérifier). |
