# Cœur RDF

Le démonstrateur vacances reste dans `agora/` (NetworkX). Le cœur à écrire pour la suite est `coeur/`.

Deux étages :

- **Connaissance** : `rdflib`, ontologies Turtle (`coeur/ontologies/`), requêtes SPARQL nommées (`coeur/requetes/`).
- **Recherche** : Python. `definir_regles`, `definir_succes`, `sonder`, `chercher_consensus`.

`ajouter_noeud` et `ajouter_lien` sont la seule porte d'écriture. Une classe ou une relation absente de l'ontologie est refusée. Les mots d'un domaine (vacances, restaurant) n'apparaissent que dans les fixtures de test.

Le veto par défaut est un coût de 100. Il ne retire pas l'option. Le chemin peut tester une concession ; il n'efface pas le veto.

```bash
pytest tests/test_coeur.py
```
