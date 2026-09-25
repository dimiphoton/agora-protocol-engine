# Expérience F — Encodage des choix de négociation

## Hypothèse

Les règles (prix du veto, rounds, anonymat, rétribution, métrique de
fitness) ne doivent **pas** être hard-codées (échange 14 + 323). Un vote
préliminaire / une config YAML choisit le *jeu* avant de jouer.

Le brainstorming appelle ça la **méta-négociation** : sous-dimensionner un
conflit identitaire ou sur-dimensionner un litige de voisinage sont deux
échecs.

Pas de blockchain : la config est un artefact off-chain, journalisable plus
tard (hash on-chain).

## Lancer

```bash
cd experiments/negociation_encodage
python proto.py
python proto.py --config copropriete.yaml
python -m pytest test_proto.py -q
```

## Lecture des chiffres

| Métrique | Sens |
|---|---|
| `rounds_joues` | Longueur réelle (peut s'arrêter avant `rounds` si H sous le seuil). |
| `vetos_declenches` | Combien de fois le prix a été payé. |
| `cout_veto_total` | Tokens brûlés. |
| `retributions` | Tokens distribués (vote, concession, bonus ΔH). |
| `anonymat` | Si vrai, les logs n'exposent pas les noms — seul le moteur les voit. |
| `least_misery_final` | Qualité de l'accord trouvé sous ces règles. |
