# Mathématiques du compromis

Les chiffres affichés par l’interface (least misery, moyenne, pénalité, dispersion, entropie) sont ceux de ce document. Le code est dans `agora/core/scores.py`.

Échelle d’une note : **-10 à +10**. Une case vide n’entre pas dans la moyenne. Zéro note connue donne une satisfaction de 0.

## Satisfaction individuelle

Pour un participant \(i\) et un candidat \(c\), après lecture du graphe (héritage `sous_type`, propagation `implique`) :

\[
s_i(c) = \text{moyenne des notes connues de } i \text{ sur } c
\]

## Veto comme coût

Un veto qui touche le candidat ne le retire pas du classement. Coût fixe \(V = 100\) :

\[
s_i^{\text{ajuste}}(c) = s_i(c) - 100 \times (\text{nombre de veto de } i \text{ sur } c)
\]

La pénalité du candidat est la somme de ces coûts. Avec beaucoup de monde, un refus écrase le score au lieu de vider l’espace.

## Scores collectifs

\[
\begin{align*}
\text{least misery}(c) &= \min_i s_i^{\text{ajuste}}(c) \\
\text{moyenne}(c) &= \text{moyenne}_i s_i^{\text{ajuste}}(c) \\
\text{pénalité}(c) &= \sum_i 100 \times (\text{veto de } i \text{ sur } c) \\
\text{dispersion}(c) &= \text{écart-type population des } s_i^{\text{ajuste}}(c)
\end{align*}
\]

L’écart-type est celui de NumPy avec `ddof=0` (diviser par \(n\), pas par \(n-1\)).

Le classement trie ainsi :

1. plus grand least misery ;
2. à égalité, plus grande moyenne ;
3. à égalité, plus petite dispersion ;
4. à égalité, plus petite pénalité.

## Exemple chiffré

Deux personnes, deux candidats. Notes déjà connues.

| | A | B |
|---|---:|---:|
| personne 1 | 8 | 2 |
| personne 2 | -2 | 6 |
| veto | aucun | la personne 1 refuse B |

A :

- least misery = min(8, -2) = **-2**
- moyenne = (8 + -2) / 2 = **3**
- pénalité = **0**
- dispersion = écart-type de {8, -2} = **5**

B, après veto :

- personne 1 : 2 - 100 = **-98**
- personne 2 : 6
- least misery = **-98**
- moyenne = (-98 + 6) / 2 = **-46**
- pénalité = **100**

A est devant. B reste dans le tableau, tout en bas. C’est le scénario « Limite : veto » de l’interface : le favori de la moyenne peut perdre, sans disparaître.

## Ce que montre « Vacances, 3 personnes »

Graine 0, simulation. Au round 5 le compromis est Bretagne, hôtel, vélo.

Satisfactions ajustées : Alice 4,30 ; Samir 5,67 ; Léa 3,00.

- least misery = **3,0** (Léa, la moins satisfaite)
- moyenne = (4,30 + 5,67 + 3,00) / 3 = **4,32**
- pénalité = **0** (personne ne veto ce trio)
- dispersion ≈ **1,09**

Un autre trio (Méditerranée, hôtel, vélo) a le même least misery 3,0 mais une moyenne plus basse (3,77). La Bretagne gagne au deuxième critère.

## Entropie d’incertitude

On prend le least misery des 20 meilleurs candidats, noté \(F_k\).

\[
z_k = F_k - \min(F) + 10^{-9}
\quad
p_k = z_k / \sum_j z_j
\quad
H_{\text{classement}} = - \sum_k p_k \ln p_k
\]

\[
\text{taux manquant} = \frac{\text{cases sans note directe}}{\text{participants} \times \text{options}}
\quad
H_{\text{round}} = H_{\text{classement}} + \text{taux manquant}
\]

\(H_{\text{round}}\) baisse quand un candidat se détache et quand les notes se remplissent. Ce n’est pas une garantie : un nouveau vote peut rouvrir le classement. L’entropie est affichée, elle n’arrête pas la recherche.

Sur la simulation vacances à 3, \(H_{\text{round}}\) passe d’environ 3,44 (beaucoup de cases vides) à **2,71** au round 5 (taux manquant 0,125).

## Exploration et arrêt

- Au plus 2000 combinaisons valides : on les note toutes.
- Au-delà : algorithme génétique (40 solutions, 40 générations maximum, arrêt si le meilleur ne bouge plus pendant 8 générations). Les mutations restent des combinaisons autorisées par le graphe (`requiert`, `incompatible`).

La négociation simulée s’arrête si le même meilleur candidat tient **3 rounds** d’affilée, ou au bout de **8 rounds**.

## Limites

- Le least misery protège la personne la moins satisfaite. Il ignore presque les gens déjà contents.
- \(V = 100\) est un choix du MVP, pas une mesure morale. Un veto pèse plus que n’importe quelle note entre -10 et 10.
- Les notes manquantes valent 0 seulement s’il n’y a aucune note. Sinon elles sont ignorées : un avis partiel peut sembler plus sûr qu’il n’est. Le taux manquant sert à le montrer.
- L’entropie utilise le least misery, pas l’ordre complet (moyenne, dispersion). Deux candidats au même minimum et à des moyennes différentes comptent pareil dans \(H\).
- Le génétique ne promet pas le meilleur candidat quand l’espace est grand. L’interface indique le mode (`exhaustif` ou `genetique`).
