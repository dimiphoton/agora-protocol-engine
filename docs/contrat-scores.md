# Contrat de scores (à coder tel quel)

Référence pour le core, les tests et la doc math. Les noms de fonctions ci-dessous sont le contrat.

Échelle de satisfaction : **-10 à +10**. Une préférence manquante n’entre pas dans la moyenne des critères. Elle augmente l’incertitude (voir entropie).

## Satisfaction d’un participant

Pour un candidat `c` et un participant `i`, après inférence sur le graphe :

```text
notes_i(c) = notes connues sur les attributs de c (directes ou héritées)
s_i(c) = moyenne(notes_i(c))    si au moins une note
s_i(c) = 0                      si aucune note
```

Veto sur un attribut présent dans `c` : **le candidat n’est pas retiré**.

```text
V = 100
penalite_i(c) = V * (nombre de veto de i qui touchent c)
s_i_ajuste(c) = s_i(c) - penalite_i(c)
```

## Agrégats

```text
least_misery(c) = min sur i de s_i_ajuste(c)
moyenne(c)      = moyenne sur i de s_i_ajuste(c)
penalite(c)     = somme sur i de penalite_i(c)
dispersion(c)   = écart-type (population, ddof=0) des s_i_ajuste(c)
```

`fitness(c)` pour le classement et la recherche :

1. plus grand `least_misery` ;
2. à égalité, plus grande `moyenne` ;
3. à égalité, plus petite `dispersion` ;
4. à égalité, plus petit `penalite`.

## Exploration

- Si le nombre de combinaisons valides (après `requiert` / `incompatible`) est **≤ 2000** : énumération exhaustive.
- Sinon : algorithme génétique. Génome = une valeur par dimension du domaine, mutation et croisement qui restent dans les combinaisons valides. Population 40, max 40 générations, arrêt anticipé si la meilleure fitness ne progresse pas pendant 8 générations.

## Arrêt d’une négociation simulée

Un round ajoute des préférences (simulateur ou saisie). On s’arrête si :

- le meilleur candidat est le même depuis **3 rounds**, ou
- le nombre de rounds atteint **8**.

L’entropie n’arrête pas la recherche. Elle s’affiche.

## Entropie d’incertitude d’un round

`F` = fitness des candidats encore classés (au plus les 20 meilleurs). On décale pour être positif :

```text
z_k = F_k - min(F) + 1e-9
p_k = z_k / somme(z)
H_classement = - somme(p_k * log(p_k))     # log naturel
taux_manquant = cases de préférence vides / cases possibles
H_round = H_classement + taux_manquant
```

`H_round` baisse quand un candidat se détache et quand les prefs se remplissent. La baisse n’est pas garantie d’un round à l’autre.

## Exemple chiffré (à reprendre dans la doc math)

Deux participants, deux candidats, notes déjà inférées.

| | A | B |
|---|---:|---:|
| s1 | 8 | 2 |
| s2 | -2 | 6 |
| veto | aucun | P1 veto B |

- A : least misery = -2, moyenne = 3, pénalité = 0
- B ajusté : s1 = 2 - 100 = -98, s2 = 6, least misery = -98, moyenne = -46, pénalité = 100

A gagne. B reste dans le classement, écrasé par le coût de veto.

## Frontières (préparer le génétique)

Deux ensembles, à ne pas confondre.

```text
X = produit cartésien des allèles          # avant le graphe
F = { c dans X : combinaison_valide(c) }   # domaine du génétique
A(τ) = { c dans F : least_misery(c) >= τ } # région acceptable, τ = 0 par défaut
```

- **Frontière dure** : `c` dans `F` qui a un voisin (un seul gène changé) hors de `F`. C'est le mur `requiert` / `incompatible`. Le génétique n'a pas le droit de le franchir.
- **Falaise de veto** : `c` dans `F` avec `penalite(c) > 0`. Le point reste dans `F`. Le saut de score vaut `V = 100`.
- **Frontière acceptable** : `c` dans `A(τ)` qui a un voisin dans `F` mais pas dans `A(τ)`.
- **Pareto** : `c` dans `F` tel qu'aucun autre point de `F` n'améliore toutes les satisfactions ajustées, et une strictement. Le least misery est une scalarisation de ce front, pas le front lui-même.

**Marge d'un allèle** : meilleur `least_misery` parmi les `c` de `F` qui fixent cet allèle. Un allèle dont cette marge est sous `τ` ne mène jamais dans `A(τ)`.

**Coupe** : deux dimensions les plus riches. Chaque case affiche le max du least misery sur les autres gènes. Case vide = aucun génome valide.

Si `|X| > 8000`, la carte n'est pas construite : c'est le régime de l'algorithme génétique, pas de l'énumération.

Fonction : `analyser_frontieres(scenario, preferences, seuil=0)`.
Commande : `python -m agora.cli frontieres veto`.
