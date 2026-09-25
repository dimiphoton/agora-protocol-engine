# Chemins de négociation

Le cœur ne se contente plus de classer des candidats. À chaque tour il **teste des chemins** sur le graphe, puis il y écrit le résultat. Le graphe du domaine est le point de départ. Les conversations l'enrichissent.

## Ce qui est ajouté au graphe

À chaque tour :

- un nœud `conversation` ;
- un nœud `chemin` par essai, relié par `teste` ;
- un nœud `direction` pour l'essai retenu, relié par `retient`.

On relit ces nœuds avec `lire_chemins` et `lire_direction`. La fonction qui lance les essais est `essayer_chemins`. Ils ne vivent pas dans une liste parallèle.

## Essais

Depuis le meilleur candidat courant :

- **proposer** : un voisin valide (un gène changé). Gain = nouveau least misery − least misery actuel.
- **conceder** : on retire un veto le temps du calcul. Gain = hausse du least misery si ce refus devient négociable. Le veto réel n'est pas effacé.
- **questionner** : une case vide, d'abord chez la personne la moins satisfaite, sur un attribut du candidat courant. On essaie les notes +10 et −10. Le gain est l'écart entre les deux least misery.

La direction retenue est le progrès réel le plus fort (`proposer` ou `conceder`). S'il n'y en a pas, la question la plus sensible. Sinon `tenir`.

## Limite

Sur un grand espace, les concessions et les questions re-notent les génomes déjà visités (exhaustif ou population génétique). Elles ne ré-énumèrent pas tout le produit.
