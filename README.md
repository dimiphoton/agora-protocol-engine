# agora-protocol-engine

Moteur de compromis : un groupe choisit entre des options, le programme cherche celle qui frustre le moins la personne la moins satisfaite.

Le démonstrateur (vacances, restaurant, week-end) vit dans `agora/` avec NetworkX : voir [docs/decision-kr.md](docs/decision-kr.md). Le cœur RDF pour la suite est `coeur/` : [docs/coeur.md](docs/coeur.md). Les formules des chiffres affichés sont dans [docs/math-consensus.md](docs/math-consensus.md). Les chemins testés sur le graphe (proposition, concession, question) sont dans [docs/chemins-negociation.md](docs/chemins-negociation.md).

## Lancer en local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run agora/app.py
```

Dans la barre latérale : choisir un scénario, **Simuler** ou **Saisir**, lire le compromis et les courbes. La version git (tag ou sha) est en bas de la barre.

Sans interface :

```bash
python -m agora.cli scenarios
python -m agora.cli run vacances_3 --simuler --seed 0
python -m agora.cli run veto --prefs prefs.json
```

Le JSON imprimé contient le meilleur candidat, l’historique des rounds et l’accord. Pour coller des préférences depuis l’interface : section « Pour un script ».

Tests : `pytest`.

## Mettre en ligne (Streamlit Community Cloud)

Le fichier lu par Streamlit est `requirements.txt` (sans les outils de scraping). Fichier principal : `agora/app.py`.

1. Ouvrir [share.streamlit.io](https://share.streamlit.io) et se connecter avec GitHub.
2. **Create app** : dépôt `agora-protocol-engine`, branche `MVP` (après fusion), main file path `agora/app.py`.
3. **Deploy**. Si un réglage avancé demande la version de Python : 3.12.

## Hugging Face Spaces

1. **New Space**, SDK **Streamlit**.
2. Déposer `agora/`, `requirements.txt`, et indiquer `agora/app.py` comme application.
3. Laisser le Space se construire. Les secrets ne sont pas nécessaires.

Les scripts de l’ancien scraping (`scripts/`) utilisent `requirements-scrape.txt`, pas le déploiement.
