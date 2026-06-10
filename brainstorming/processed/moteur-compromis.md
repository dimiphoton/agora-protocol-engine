# Moteur De Compromis

Source brute : `brainstorming/raw/gemini-ontologie-pour-la-recherche-de-compromis.md`

Ce fichier regroupe les échanges sur l'algorithme central : comment chercher un compromis à partir de préférences, contraintes, votes, veto et incertitude.

## Map Of Content

- [But du Bloc](#but-du-bloc)
- [Échanges À Relire](#échanges-à-relire)
- [Sous-Blocs](#sous-blocs)
- [Fiches D'Échanges](#fiches-déchanges)
- [Concepts Clés](#concepts-clés)
- [Architecture Algorithmique](#architecture-algorithmique)
- [Décisions À Prendre](#décisions-à-prendre)
- [À Extraire En Code](#à-extraire-en-code)

## But Du Bloc

Le moteur de compromis doit répondre à une question simple :

> Parmi plusieurs solutions possibles, laquelle réduit le mieux les frustrations, respecte le mieux les contraintes et augmente le plus la possibilité d'un accord ?

Il ne doit pas seulement compter des votes. Il doit guider une recherche progressive.

## Échanges À Relire

| Lien brut | Question abrégée | Réponse abrégée |
|---|---|---|
| [Échange 3](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-3) | Peut-on définir une descente de gradient vers un consensus ? | Non au sens strict ; l'esprit d'amélioration progressive reste valable dans un espace discret. |
| [Échange 5](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-5) | Comment passer à beaucoup d'options et de participants ? | Utiliser une exploration de type algorithme génétique plutôt qu'un balayage exhaustif. |
| [Échange 6](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-6) | Comment combiner algorithme génétique et frontières non négociables ? | Distinguer l'explorateur de solutions et le module de contraintes qui définit le terrain valide. |
| [Échange 7](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-7) | Un participant peut toujours bloquer quand le groupe grossit. | Transformer le veto absolu en coût, pénalité ou signal de négociation. |
| [Échange 12](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-12) | Comment casser le concept de budget pour trouver une marge ? | Chercher des reformulations et contreparties qui déplacent la frontière. |
| [Échange 72](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-72) | Le token matérialise-t-il un dividende de paix et un nouvel équilibre ? | Le protocole change la matrice d'incitations pour rendre la coopération plus rationnelle. |
| [Échange 73](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-73) | La recherche de consensus utilise-t-elle toujours Nash ? | Non ; Nash analyse un jeu, le consensus conçoit un mécanisme vers Pareto ou optimum social. |
| [Échange 100](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-100) | Exemple d'habitude perçue comme belliqueuse : comment émergent les propositions ? | Les propositions peuvent venir d'une combinaison IA, citoyens, rôles et contreparties. |
| [Échange 103](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-103) | Comment éviter le spam de propositions par des geeks ? | Nécessité de filtres, coût d'action, réputation ou sélection des propositions utiles. |
| [Échange 108](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-108) | Le système doit proposer lui-même des pistes, pas seulement attendre les humains. | L'IA peut générer des candidats, mais la fitness doit rester évaluée par sondage humain. |
| [Échange 115](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-115) | Traduire le projet en théorie de l'information avec compteur d'entropie. | L'entropie peut mesurer incertitude, dispersion et progression de la négociation. |
| [Échange 119](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-119) | Qu'est-ce qui change vraiment avec la théorie de l'information ? | Elle aide à choisir les questions, valoriser les pistes et lire la convergence. |
| [Échange 189](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-189) | Revenir à l'entropie comme aide à la valorisation des récompenses. | L'entropie sert surtout d'indicateur pour débloquer, synthétiser et orienter. |
| [Échange 311](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-311) | Comment intégrer Axelrod, coopération, trahison, pardon, ESS ? | Ces stratégies peuvent inspirer des comportements de simulation, mais complexifient le core. |
| [Échange 322](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-322) | Faut-il toujours refuser les ultimatums ? | Les ultimatums peuvent être analysés comme signaux, contraintes ou mauvais formats de négociation. |
| [Échange 323](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-323) | Créer un processus préliminaire pour choisir la complexité de la négociation. | Idée d'un méta-processus qui décide du format avant de traiter le fond. |

## Sous-Blocs

### 1. Score De Consensus

Le score peut combiner plusieurs métriques :

- moyenne des satisfactions ;
- `least misery`, c'est-à-dire maximiser la satisfaction du participant le moins satisfait ;
- nombre de veto ;
- intensité des objections ;
- progression par rapport au round précédent.

Pour le MVP, il faut garder un score lisible, quitte à ajouter des variantes ensuite.

### 2. Contraintes Et Veto

Un point récurrent : si chaque veto est absolu, le système peut être bloqué.

Pistes de traitement :

- élimination stricte dans un petit MVP ;
- pénalité massive dans une version plus réaliste ;
- demande de justification ;
- recherche de marge de négociation ;
- compensation ou reformulation.

### 3. Algorithme Génétique

L'algorithme génétique est utile quand l'espace des solutions devient trop grand.

Structure :

- générer une population de solutions candidates ;
- évaluer chaque solution ;
- conserver les meilleures ;
- croiser des solutions ;
- muter certaines dimensions ;
- relancer un round.

Dans le MVP vacances, ce n'est pas indispensable au départ, mais c'est la bonne direction pour passer à l'échelle.

### 4. Sondage Et Fitness

La fitness n'est pas forcément connue à l'avance. Elle peut être apprise par sondages successifs.

Le système peut demander :

- “Que pensez-vous de cette option ?”
- “Cette contrainte est-elle absolue ?”
- “Accepteriez-vous cette concession si une autre condition est satisfaite ?”
- “Cette nouvelle solution améliore-t-elle votre situation ?”

Le moteur ne connaît donc pas tout : il explore, sonde et met à jour.

### 5. Entropie

L'entropie apparaît comme une mesure de désordre, d'incertitude ou de dispersion des préférences.

Usage possible :

- prioriser les questions les plus informatives ;
- repérer les zones de blocage ;
- mesurer si une négociation converge ;
- rémunérer certaines actions qui réduisent l'incertitude.

Prudence : l'entropie ne doit pas remplacer le jugement politique ou moral. Elle sert d'indicateur.

### 6. Négociation Du Format

Les derniers échanges reviennent sur une idée forte : avant de négocier le contenu, il faut parfois négocier le format de la négociation.

Questions possibles :

- Le conflit est-il surtout matériel, symbolique, territorial, économique ?
- Faut-il un processus simple ou complexe ?
- Faut-il séparer plusieurs dimensions ?
- Faut-il traiter d'abord les urgences, les identités, l'argent, la justice ?

## Fiches D'Échanges

### Échange 3 - Descente De Gradient Ou Pas ?

Lien brut : [Échange 3](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-3)

**Ta question (verbatim) :**

> mon idée c'est vraiment que la structure de donnée ait une capacité de sonder les participant, de manière illimitée, désynchronisée. est-il facile selon-toi de définit une "descente de gradient" pour chercher un consensus?

**Ce que tu cherches :** tu insistes sur un sondage illimité et désynchronisé, et tu cherches une analogie mathématique : une descente de gradient vers le consensus.

**Réponse Gemini :** Gemini répond que non, une descente de gradient *classique* n'est pas facile car ton espace n'est pas continu ni différentiable (on ne peut pas « augmenter un peu l'Hôtel A »), mais que *l'esprit* de la méthode est le bon. Il pose deux ingrédients : une **fonction de coût** (par ex. la satisfaction de la personne la moins satisfaite, à minimiser) et un **processus itératif** (proposer → sonder → calculer le coût → générer une meilleure solution). Faute de gradient mathématique, il oriente vers des méthodes d'optimisation discrète/combinatoire.

**Mise en contexte :** cet échange clarifie que le moteur ne doit pas être pensé comme une optimisation numérique pure. On ne minimise pas simplement une fonction mathématique connue.

**Mon avis :** la bonne intuition à garder est “amélioration progressive”, pas “gradient”. Pour coder, il vaut mieux partir sur recherche locale, génération de candidats, scoring, puis rounds de sondage.

### Échange 6 - Algorithme Génétique Et Contraintes

Lien brut : [Échange 6](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-6)

**Ta question (verbatim) :**

> tu as proposé un algorithme génétique. je te remercie de me l'apprendre. je ne connais pas du tout, explique. Aussi, je pensais programmer la structure pour qu'elle sonde les marges de négociation possibles, c'est-à-dire sonder les valeur ( je ne sais pas comment l'exprimer: un programme peut -être acceptable, ou non négotiable) et en déduire une géométrie de frontières à ne pas dépasser

**Ce que tu cherches :** tu veux comprendre l'algorithme génétique, mais tu ajoutes une intuition plus importante : sonder les frontières, les marges et les valeurs non négociables pour en déduire une géométrie de l'espace acceptable.

**Réponse Gemini :** (échange 6) Gemini distingue le moteur d'**exploration** (algorithme génétique) et la **définition de l'espace** par contraintes, et détaille l'AG (génome, population, fitness, sélection/croisement/mutation), en soulignant que tes frontières le rendent bien plus efficace.

**Mise en contexte :** c'est une architecture importante : exploration et contraintes ne sont pas la même chose.

**Mon avis :** c'est une excellente base technique. Dans le code, il faut éviter une grosse fonction monolithique. Il faut séparer `candidate_generation`, `constraint_checking` et `scoring`.

### Échange 7 - Le Problème Du Veto

Lien brut : [Échange 7](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-7)

**Ta question (verbatim) :**

> oui, sauf que comme le nombre de participants va croissant, il faudra redéfinir ce qui constitue une frontière car il y a toujours 1 personne qui peut bloquer.

**Ce que tu cherches :** tu pointes la faille du veto absolu : avec beaucoup de participants, il y a toujours quelqu'un pour bloquer, donc la notion de frontière doit être redéfinie.

**Réponse Gemini :** (échange 7) Gemini nomme ton problème le « paradoxe du dictateur » / tyrannie de la minorité : si chacun pose une frontière absolue, l'espace acceptable devient nul. Sa solution : ne jamais traiter une frontière comme un mur, mais comme un **coût de veto**, c'est-à-dire une pénalité massive (ex. -1000) qui n'élimine pas la solution mais l'écrase dans le score `least misery`, ce qui pousse l'algorithme génétique à l'éviter naturellement.

**Mise en contexte :** c'est un point central pour tout moteur de compromis réel. La négociation ne peut pas être une accumulation mécanique de refus.

**Mon avis :** le MVP peut tester les veto stricts, mais le moteur final doit représenter plusieurs intensités d'objection. Sinon une seule personne peut bloquer tout le système.

### Échanges 72-74 - Nash, Pareto Et Optimum Social

Liens bruts : [Échange 72](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-72), [Échange 73](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-73), [Échange 74](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-74)

**Tes questions (verbatim) :**

> dans la philosophie du projet, tu as insisté que c'est une négociation, donc une optimisation de l'utilité ou de consensus ou quelque chose comme ca. Je suis encore influencé par ma vision de l'équilibre de Nash. c'est comme si ce token matérialisait les dividendes de la paix. explique, corrige.

> attends attends ... je croyais que l'équilibre de Nash était la mauvaise manière d'aborder le sujet. et là tu me dis que c'est un peu équivalent. Est-ce que la recherche de consensus utilise toujours le formalisme de Nash?

**Ce que tu cherches :** tu es encore influencé par l'équilibre de Nash et tu sens une contradiction. Tu veux qu'on corrige le bon formalisme : optimisation d'utilité, consensus, Pareto, ou Nash ?

**Réponse Gemini :** Gemini commence par valider ton intuition (échange 72) : dans un conflit, l'équilibre de Nash est `(Trahir, Trahir)` — stable mais terrible. Le protocole ne cherche pas un équilibre dans la matrice existante, il **change la matrice** en y injectant le « dividende de la paix » matérialisé (token $PACT). Puis, face à ta relance (échange 73), il tranche clairement : « non, la recherche de consensus n'utilise PAS le formalisme de Nash ». Il oppose Nash, outil d'**analyse** de jeux non coopératifs (joueurs égoïstes qui ne se font pas confiance), à la recherche de consensus, outil de **conception** issu de la théorie des jeux coopérative / choix social, qui vise un **optimum de Pareto ou social**.

**Mise en contexte :** ces échanges changent le vocabulaire du projet. On ne cherche pas seulement un état stable ; on cherche un processus qui fabrique les conditions d'un meilleur accord.

**Mon avis :** pour le MVP, il ne faut pas commencer par Nash. Il faut expliquer en termes simples : “on cherche la solution qui crée le moins de frustration et le plus d'acceptabilité”.

### Échanges 100-112 - Propositions, Calcul Et Confiance

Liens bruts : [Échange 100](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-100), [Échange 104](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-104), [Échange 108](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-108), [Échange 110](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-110)

**Tes questions (verbatim) :**

> imaginons un exemple précis: une habitude (chant, programme d'endoctrinement) de la pop A est perçue par la pop B comme belliqueuse. Dans cette négociation, comment émergerait la proposition (ou le noeud, comme tu veux) "mettre fin à cette habitude?" [...] est-ce qu'elle serait détectée par un rôle? est-ce qu'elle serait formulée par la foule (c-a-d un geek)? ou autrement?

> on est en désaccord. le projet d'ontologie+blockchain+algorithme génétique devrait proposer des pistes par lui-même . l'intervention humaine était censée être dans l'ontologie et bien sûr les votes

> dans tes réponses précédentes, tu pensais vraiment coder les poids et marges des intervenants directement? ma philosophie est de sonder et de rester émergent.

**Ce que tu cherches :** tu contestes l'idée que tout viendrait d'humains, ou que les poids seraient codés en dur. Tu veux que le système propose lui-même des pistes en explorant l'ontologie, et que l'humain n'intervienne que via l'ontologie et les votes. Le mot-clé est "émergent".

**Réponse Gemini :** Sur le cas du « chant perçu comme belliqueux » (échange 100), Gemini fait émerger la proposition par une chaîne de rôles humains puis l'IA : un `Plaignant`/`Délégué` ouvre un « grief ciblé » (en dépensant du $NEGO pour éviter le spam), un `Avocat` rémunéré attache un « raisonnement sémantique » prouvant le lien via l'ontologie. Puis (échange 108), face à ta vision émergente, il propose la **« fitness pilotée par l'ontologie » (ODF)** : au lieu de faire noter l'humain en boucle, on code les préférences et vetos *dans le graphe lui-même*, déplaçant l'effort du vote répétitif vers la modélisation sémantique.

**Mise en contexte :** c'est un passage confus mais précieux : il révèle une tension réelle entre IA génératrice, foule, blockchain et confiance.

**Mon avis :** la bonne synthèse est : l'IA génère des candidats, les humains évaluent, la blockchain peut enregistrer les étapes importantes plus tard. Le MVP doit simuler cette boucle sans blockchain.

### Échanges 115-124 - Entropie

Liens bruts : [Échange 115](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-115), [Échange 119](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-119), [Échange 189](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-189)

**Tes questions (verbatim) :**

> pourrais-tu essayer de traduire l'ensemble de ce projet avec les termes de la théorie de l'information? je pense même qu'un compteur d'entropie serait possible

> ok on revient à l'entropie. pour moi c'est juste une aide à la valuation des récompenses . je pense aussi que ca permettrait de synthétiser l'avancement et de débloquer des récompenses intermédiaires. est-ce que le progrès est monotone avec l'entropie globale?

**Ce que tu cherches :** tu pressens qu'un compteur d'entropie pourrait mesurer l'avancement, valoriser des pistes et débloquer des récompenses. Tu te poses même la question de la monotonie du progrès par rapport à l'entropie.

**Réponse Gemini :** Gemini traduit le projet en théorie de l'information (échange 115) : le conflit est un état de **haute entropie**, la négociation un **gain d'information** qui la réduit, l'accord un état de basse entropie (≈0) ; l'IA devient un « moteur de compression d'information ». Il donne un dictionnaire (ontologie = alphabet/capacité du canal, fatigue = bruit). Puis (échange 119) il montre ce que ça change : l'AG n'explore plus à l'aveugle mais est **dirigé vers les zones de haute entropie** (plus grand gain potentiel), et le sondage devient une **élicitation active** qui questionne là où l'incertitude est forte, réduisant la fatigue. Enfin (échange 189) il valide que l'entropie sert à **tarifer les récompenses** (une action qui fait chuter l'entropie est rare et bien payée) et à **débloquer des rounds** par paliers.

**Mise en contexte :** c'est une très bonne idée, mais elle arrive après le score de compromis. L'entropie mesure le processus, pas seulement la qualité d'une solution.

**Mon avis :** à garder en version 2. Elle peut servir à choisir la prochaine question à poser. Mais pour la version 1, un score lisible est plus important.

### Échanges 322-329 - Négocier Le Format

Liens bruts : [Échange 322](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-322), [Échange 323](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-323)

**Tes questions (verbatim) :**

> Parlons des ultimatums. Mon projet est parti de l'idée de globalement les refuser et préférer une convergence vers l'utilité maximale. Mais je peux me tromper. Developpe une réflexion théorique et pratique

> J'ai une autre idée: un processus préliminaire pour decider de la complexité du processus de négociation. Explore theorie et pratique

**Ce que tu cherches :** tu remets en question ton propre refus des ultimatums, et tu proposes une étape préliminaire qui déciderait de la complexité de la négociation elle-même. C'est l'idée d'un méta-processus.

**Réponse Gemini :** Sur les ultimatums (échange 322), Gemini valide ton intuition mais nuance : l'ultimatum a trois fonctions réelles (forcer la convergence / *stopping rule*, signaler une vraie limite, et la dignité morale — cf. le jeu de l'ultimatum où l'on refuse 1€ pour punir l'injustice). Il propose donc de ne pas l'interdire mais de le **désarmer**. Sur ta seconde idée (échange 323), il la baptise **« méta-négociation »** (négocier sur la négociation) et la justifie par la loi d'Ashby (variété requise) et le coût de transaction cognitif : un « sas de triage » préliminaire (≤24h) choisit le niveau de complexité du processus pour éviter le sous- ou sur-dimensionnement.

**Mise en contexte :** c'est une idée avancée, mais très importante pour les conflits lourds.

**Mon avis :** ce n'est pas pour le MVP vacances. En revanche, c'est une future brique forte : `choose_negotiation_protocol(conflict_profile)`.

## Concepts Clés

- **Optimum de Pareto** : situation où on ne peut pas améliorer quelqu'un sans détériorer quelqu'un d'autre.
- **Optimum social** : solution globalement bonne selon une fonction collective.
- **Équilibre de Nash** : état stable où personne n'a intérêt à changer seul, mais qui peut être mauvais collectivement.
- **Mechanism design** : conception des règles du jeu pour rendre certains comportements plus probables.
- **Fitness** : score d'une solution candidate.
- **Entropie** : mesure de dispersion, d'incertitude ou de désordre.

## Architecture Algorithmique

Flux minimal :

```text
options candidates
  -> sondage des participants
  -> calcul des scores
  -> détection des objections fortes
  -> génération de nouvelles options
  -> nouveau round
```

Flux plus avancé :

```text
ontologie + contraintes + historique des votes
  -> génération de candidats
  -> calcul fitness
  -> mesure entropie
  -> choix des questions utiles
  -> ajustement des frontières
  -> sélection / mutation / bifurcation
```

## Décisions À Prendre

- Le score initial doit-il être `least misery`, moyenne pondérée, ou hybride ?
- Un veto supprime-t-il une option ou ajoute-t-il une pénalité ?
- Le système propose-t-il lui-même des options ou trie-t-il seulement des options humaines ?
- À quel moment considère-t-on qu'un accord est assez bon ?
- L'entropie est-elle seulement affichée ou utilisée dans le calcul ?

## À Extraire En Code

Fonctions candidates :

```python
def generate_candidates(domain: dict) -> list[dict]:
    ...

def score_candidate(candidate: dict, preferences: dict) -> float:
    ...

def detect_blockers(candidate: dict, preferences: dict) -> list[str]:
    ...

def rank_candidates(candidates: list[dict], preferences: dict) -> list[dict]:
    ...

def choose_next_questions(candidates: list[dict], uncertainty: dict) -> list[str]:
    ...
```

## Risque Principal

Construire un moteur trop abstrait avant d'avoir un cas test simple. La bonne séquence est : score simple, simulation, puis enrichissement.

