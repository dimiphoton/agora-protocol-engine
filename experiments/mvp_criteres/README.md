# Expérience G — Critères, MVPs, synthèse

Cette branche ne fusionne pas le code de A–F (chaque proto reste sur
sa branche). Elle **interprète** leurs chiffres + le brainstorming.

## Lancer

```bash
cd experiments/mvp_criteres
python proto.py
python -m pytest test_proto.py -q
```

## Documents

- `SYNTHESIS.md` — le projet tel que le brainstorming le décrit, réponses
  aux 4 questions, recommandation d'architecture, liste MVP, trop tôt.
- `proto.py` — cadre de mesure (utilité, efficacité, coût cognitif,
  temps à consensus, robustesse au veto) et classement des MVPs.

Les scores MVP sont une **grille transparente**, pas une vérité. Les
entrées numériques viennent des runs A–F (2026-09-25).
