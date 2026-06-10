# Ontologie & Sémantique

Source brute : `brainstorming/raw/gemini-ontologie-pour-la-recherche-de-compromis.md`

Ce fichier regroupe les échanges sur la représentation du sens : ontologies, graphes, récits, valeurs, catégories et relations entre concepts.

## Map Of Content

- [But du Bloc](#but-du-bloc)
- [Échanges À Relire](#échanges-à-relire)
- [Sous-Blocs](#sous-blocs)
- [Fiches D'Échanges](#fiches-déchanges)
- [Types D'Ontologies](#types-dontologies)
- [Graphe De Connaissance](#graphe-de-connaissance)
- [Décisions À Prendre](#décisions-à-prendre)
- [À Extraire En Spec](#à-extraire-en-spec)

## But Du Bloc

L'ontologie est ce qui permet au projet de ne pas être un simple tableur de votes.

Elle sert à représenter :

- les objets du problème ;
- les relations entre ces objets ;
- les valeurs et récits des participants ;
- les contraintes implicites ;
- les reformulations possibles.

## Échanges À Relire

| Lien brut | Question abrégée | Réponse abrégée |
|---|---|---|
| [Échange 1](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-1) | Une ontologie autour d'un sujet peut-elle chercher un compromis ? | L'ontologie devient la structure sémantique d'un système de décision de groupe. |
| [Échange 8](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-8) | Critique : l'ontologie n'est pas vraiment utilisée. | Reprise du problème vacances comme graphe de lieux, activités, ambiances et contraintes. |
| [Échange 9](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-9) | Enrichir l'ontologie et simuler l'algorithme génétique. | L'ontologie définit l'espace de recherche ; l'algorithme génétique l'explore. |
| [Échange 14](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-14) | Éviter le hardcoding avec une ontologie collaborative type Wikipédia. | Idée d'un graphe enrichi par la communauté, mais nécessitant validation et gouvernance. |
| [Échange 16](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-16) | Les outils existants ne gèrent pas un consensus complexe plein de sens. | Le projet doit aller au-delà d'un vote simple : conditions, clauses, sémantique. |
| [Échange 17](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-17) | Le coeur est de générer un accord qui ait du sens, presque un contrat. | L'IA doit composer des clauses et des package deals à partir d'un langage structuré. |
| [Échange 65](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-65) | Comment traiter une accusation de génocide distordue ou ressentie ? | Séparer faits, ressentis, récits, preuves et reconnaissance symbolique. |
| [Échange 66](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-66) | Que faire face à deux visions du monde incompatibles ? | L'IA peut cartographier les visions sans prétendre les fusionner immédiatement. |
| [Échange 110](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-110) | Les poids et marges ne doivent pas être codés directement. | Le système doit les apprendre par sondage et rester émergent. |
| [Échange 212](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-212) | Cas extrême : l'existence même d'un groupe est jugée illégitime. | Nécessité d'ontologies capables de représenter des récits incompatibles. |
| [Échange 213](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-213) | Y a-t-il une seule ontologie ? | Réponse vers une pluralité de couches ontologiques plutôt qu'un unique graphe total. |
| [Échange 219](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-219) | Construire un graphe Obsidian des composants du projet. | Liste de composants, rôles et liens à organiser en connaissance navigable. |
| [Échange 288](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-288) | Les drapeaux et communautés sont vus comme irréconciliables. | Possibilité de faire émerger des narratifs constructifs sans effacer les identités. |
| [Échange 339](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-339) | Présenter la blockchain de négociation tournée vers valeurs et communs. | Reformulation vers reconnaissance des valeurs, récits et communs numériques. |
| [Échange 341](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-341) | Améliorer l'email à Michel Bauwens ; éviter de suivre aveuglément les questions. | Recentrage sur les communs, le P2P et le risque de techno-solutionnisme. |

## Sous-Blocs

### 1. Ontologie De Domaine

Dans le MVP vacances, l'ontologie décrit des choses simples :

- destination ;
- logement ;
- activité ;
- budget ;
- climat ;
- distance ;
- ambiance ;
- accessibilité.

Elle permet de comprendre que `voile` est proche de `activité nautique`, ou que `camping` peut être lié à `nature`, `budget faible`, `inconfort possible`.

### 2. Ontologie De Négociation

Cette couche décrit le processus :

- participant ;
- groupe ;
- proposition ;
- concession ;
- veto ;
- contrepartie ;
- accord ;
- clause ;
- round ;
- validation.

Elle est indépendante du domaine concret.

### 3. Ontologies Politiques Et Récits

Pour les conflits lourds, une seule ontologie peut être oppressive.

La discussion insiste sur la coexistence de récits divergents :

- récit d'un groupe ;
- mémoire historique ;
- symbole ;
- drapeau ;
- territoire ;
- identité ;
- dignité ;
- injustice perçue.

L'enjeu n'est pas de forcer une vérité unique, mais de rendre les désaccords représentables.

### 4. Ontologie Objective

À côté des récits, il faut des éléments plus vérifiables :

- faits ;
- dates ;
- engagements ;
- ressources ;
- clauses ;
- paiements ;
- décisions validées ;
- preuves.

Cette ontologie peut servir de base à des contrats ou des engagements audités.

### 5. Ontologie Collaborative

L'idée apparaît d'une ontologie écrite ou enrichie par des bénévoles, un peu comme Wikipédia.

Cela pose des questions :

- qui peut modifier l'ontologie ?
- qui valide les relations ?
- comment éviter le spam ou la capture idéologique ?
- comment versionner les changements ?

## Fiches D'Échanges

### Échange 8 - “Tu N'As Pas Utilisé D'Ontologie”

Lien brut : [Échange 8](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-8)

**Ta question (verbatim) :**

> je trouve que tu n'as pas utilisé d'ontologie. je ne connais pas trop, mais je sais que ca permet de structure le problème en graphe et que ca permet d'encoder le sens. réfléchis et propose un exemple minimal de choix de vacance où une ontologie est utilisée. explique comment ca marche et concretement ce que ca permet

**Ce que tu cherches :** tu refuses que l'ontologie soit un mot décoratif. Tu rappelles ce que tu en sais (graphe, encodage du sens) et tu demandes un exemple minimal et concret sur le cas vacances.

**Réponse Gemini :** Gemini admet avoir nommé l'ontologie sans l'employer, et la présente comme un **graphe de connaissances** permettant de *raisonner*, et non une liste. Il pose des classes (`Vacance`, `Activité`, `Destination`) et des relations porteuses de sens (`est un type de`, `a pour climat`, `requiert`), avec des exemples : « Voile *requiert* Accès Mer », « Bretagne *a* Accès Mer », « Auvergne *n'a pas* Accès Mer ». Il montre un sondage par contraintes où le système **infère** des conséquences plutôt que de tout demander.

**Mise en contexte :** c'est le moment où le projet se distingue d'un système de vote multicritère classique.

**Mon avis :** ta critique est juste. Si le système ne fait que calculer des scores, l'ontologie est inutile. Elle doit produire quelque chose : filtrer, inférer, reformuler ou générer des alternatives.

### Échanges 9-10 - Enrichir Et Simuler

Liens bruts : [Échange 9](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-9), [Échange 10](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-10)

**Tes questions (verbatim) :**

> enrichis l'ontologie, puis simule une recherche par algorithme génétique

> ouah je suis satisfait. augmente la taille de l'ontologie et le nombre de participants

**Ce que tu cherches :** tu valides la direction et tu pousses la montée en charge : ontologie plus riche, plus de participants, et une vraie simulation de recherche.

**Réponse Gemini :** Gemini enrichit l'ontologie (le « cerveau ») et l'articule avec l'AG (le « moteur d'exploration »). Il ajoute des classes (`Budget`, `Transport`, `Ambiance`) et surtout des relations logiques : `requiert` (contrainte dure), `implique` (conséquence logique), `est incompatible avec` (exclusion). Exemples : « Festival *implique* Ambiance Festive et Budget Élevé », « Randonnée *est incompatible avec* Plat Pays ». Puis il simule une recherche où l'AG navigue *intelligemment* dans le monde ainsi défini, au lieu de tirer au hasard.

**Mise en contexte :** ces échanges montrent le couplage clé : l'ontologie n'est pas seulement une base de connaissances, elle sert de générateur de candidats.

**Mon avis :** c'est une très bonne architecture. En code, l'ontologie peut commencer simplement comme un dictionnaire de dimensions et relations, puis évoluer vers un graphe.

### Échange 14 - Ontologie Collaborative

Lien brut : [Échange 14](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-14)

**Ta question (verbatim) :**

> Je voudrais que mon système soit le moins hard codé possible. ainsi, l'ontologie serait écrite par des bénévoles comme wikipedia, et les délais de négociations et les regles de veto seraient décidées par un vote préliminaire au processus. as-tu d'autres idées?

**Ce que tu cherches :** tu veux le moins de hardcoding possible : une ontologie écrite par des bénévoles façon Wikipédia, et des règles (délais, veto) fixées par un vote préliminaire. Tu relies déjà sémantique et gouvernance.

**Réponse Gemini :** Gemini valide ta vision « le moins hard-codé possible » et distingue deux piliers : l'**ontologie vivante** (gérée collectivement, elle définit ce qui est *vrai*) et les **règles votées** (elles définissent ce qui est *juste*). Sa proposition forte : rendre **la métrique de consensus elle-même votable** au lieu de coder le `least misery` en dur — un vote préliminaire choisit l'objectif (prudence = least misery, utilitarisme = moyenne, enthousiasme = maximiser les coups de cœur). Il propose aussi un capital de veto dynamique et basé sur le mérite.

**Mise en contexte :** cette idée relie directement la sémantique à la gouvernance. Qui définit les mots définit une partie du processus.

**Mon avis :** très intéressant, mais pas MVP. Pour démarrer, il faut une ontologie contrôlée. La version collaborative vient plus tard, quand on sait ce qu'il faut modifier.

### Échange 17 - Accord Avec Du Sens

Lien brut : [Échange 17](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-17)

**Ta question (verbatim) :**

> le coeur de mon projet c'est la capacité de l'IA de générer un accord avec du sens, quasiment un contrat écrit. Le contrat aurait beaucoup de clause, et l'IA aurait des solutions pour éviter les blocages et matérialiser les pistes de négociations possibles. Et puisqu'il faut que les participants y trouvent un intérêt, les actions de répondre, proposer, voter pour un délégué seraient rémunérées en token

**Ce que tu cherches :** tu formules le coeur du projet : une IA qui génère un accord ayant du sens, presque un contrat à clauses, avec des mécanismes anti-blocage. Tu introduis aussi la rémunération en tokens des actions (répondre, proposer, voter).

**Réponse Gemini :** Gemini parle du « Saint Graal » d'une DAO : trouver un accord, le *formaliser* et *inciter* économiquement. Il pose trois piliers : ontologie (le « Vrai »), IA-médiateur (le « Négociateur »), token (l'« Intérêt »). Surtout, il scinde l'IA en deux temps : **(A) un optimiseur** (AG / solveur de contraintes type OptaPlanner) qui produit un *jeu de données de solution* (`SolutionID, Budget, concessions...`), puis **(B) un générateur « Notaire »** qui traduit ce jeu de données en **contrat en langage naturel** via du NLG/LLM, l'ontologie servant de *schéma* (plan) au contrat.

**Mise en contexte :** on passe d'options simples à des accords structurés. L'ontologie devient le langage dans lequel l'accord est composé.

**Mon avis :** c'est une vision très forte, mais elle exige d'abord un mini-langage de clauses. Pour le MVP vacances, une “clause” peut être une phrase simple : “destination Bretagne, logement hôtel, budget max 900 euros”.

### Échanges 65-66 - Conflits De Récits

Liens bruts : [Échange 65](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-65), [Échange 66](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-66)

**Tes questions (verbatim) :**

> comment l'IA gère une accusation de génocide distordue? (c'est à dire un sentiment plutôt que des faits)

> certains conflits naiussent de la confrontation de deux visions du monde. par exemple le droit et l'individu contre la race et le groupe. Qu'apporte cette IA? changer la vision du monde d'un groupe est colossale, mais cela pourrais être une graine de changement

**Ce que tu cherches :** tu poses des cas limites : une accusation fondée sur un ressenti plutôt que des faits, et deux visions du monde incompatibles. Tu reconnais que changer une vision du monde est colossal, mais tu y vois une graine de changement.

**Réponse Gemini :** Sur l'accusation distordue (échange 65), Gemini pose un principe : l'IA ne peut **jamais** être juge de la vérité, sous peine de perdre toute légitimité d'un côté ou de l'autre. Sa solution est le **triage sémantique** : « casser » l'accusation en deux et la router vers deux greffes — le *sentiment/traumatisme* (Round 1 Honneur, module d'attestation narrative) et le *fait/qualification légale* (Cour d'arbitrage). Sur le choc de visions du monde (échange 66), il refuse que l'IA soit un « colonisateur culturel » : elle n'apporte pas une meilleure vision mais un **espace neutre**. Elle agit en « traducteur sémantique » qui contourne le blocage et ouvre une **Bourse de Neutralisation Sémantique** où un `Lexicographe` rémunéré en $PACT invente un nouveau concept satisfaisant les intérêts des deux camps sans violer leur philosophie.

**Mise en contexte :** c'est la version politique de l'ontologie. Elle ne sert plus seulement à classer des vacances, mais à rendre explicite des visions du monde.

**Mon avis :** puissant mais très risqué. Pour éviter l'arrogance technocratique, le système devrait dire “voici les récits en conflit” plutôt que “voici la vérité”.

### Échanges 212-220 - Ontologies Multiples Et Graphe Obsidian

Liens bruts : [Échange 212](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-212), [Échange 213](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-213), [Échange 219](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-219)

**Tes questions (verbatim) :**

> Dans des cas extreme comme israel-palestine, l'existence meme d'un groupe, d'un état est vue comme illégitime, à faire disparaître. J'ai la foi que cette IA saura trouver un ch3min de négociation mais cette proposition sera formulée

> Y a-t-il une seule ontologie?

> Je voudrais ecrire dans obsidian les composants de ce projet de negociation que tu as listé. Tu comptends bien qu'il y a des liens

**Ce que tu cherches :** tu testes l'IA sur le cas le plus dur (existence niée d'un groupe), tu demandes s'il existe une seule ontologie, et tu veux construire dans Obsidian un graphe des composants reliés du projet.

**Réponse Gemini :** Sur le cas existentiel (échange 212), Gemini contourne la question de la « légitimité » par un **pragmatisme quantifié** : un « Package Deal Minimal » centré sur la survie (arrêt de tirs vérifiable par oracle, distribution de vaccins), avec le Dividende de la Paix ($PACT) comme levier. Sur ta question directe (échange 213), il répond qu'il n'y a **jamais une seule ontologie** : trois coexistent — les **ontologies privées** (réalités subjectives, ex. « terroriste » vs « combattant de la liberté »), l'**ontologie de négociation** (bac à sable neutre du Round 1, lieu de la Bourse de Neutralisation), et l'**ontologie de consensus** (le « Manuel d'Histoire Commun » final, ratifié à la double majorité). Enfin (échange 219), il se corrige et te livre la **liste structurée des composants** prête à coller dans Obsidian, avec des nœuds `[[...]]`.

**Mise en contexte :** ce passage sert à organiser le projet lui-même, pas seulement le produit.

**Mon avis :** il faut éviter trop de couches au départ. Je garderais trois catégories : ontologie du domaine, ontologie du processus, ontologie des récits. C'est déjà beaucoup.

### Échanges 288-291 - Drapeaux Et Identités

Liens bruts : [Échange 288](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-288), [Échange 290](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-290), [Échange 291](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-291)

**Ta question (verbatim) :**

> les conflits sont souvents bloqués car les drapeaux, les communautés sont vus comme irréconciliables. Il faudrait que puissent émerger des narratifs, des identités nouvelles. Donc par exemples des drapeaux nouveaux. Raisonne sur ce deklocage, ne te centre pas uniquemznt sur les drapeaux

**Ce que tu cherches :** tu vois les identités figées (drapeaux, communautés) comme une cause de blocage, et tu demandes comment faire émerger des récits et des identités nouvelles. Le drapeau n'est qu'un exemple : tu veux le mécanisme général de déblocage symbolique.

**Réponse Gemini :** Gemini relie ton idée au concept d'**identité constructiviste** : les conflits durent parce que les identités sont *figées*. Il refuse le compromis « Bleu + Rouge = violet fade » et vise l'émergence d'une **nouvelle couleur primaire** (« Or ») qui transcende les deux. Le protocole devient une « Machine à Tisser des Identités » : une greffe d'**IA générative** (LLM + génération d'images) repère les valeurs communes cachées dans l'ontologie (Terre, Famille, Honneur) et produit des **artefacts de synthèse** (nouveau nom géographique, drapeau fusionné, devise), soumis à un **« Vote de Résonance »** où l'on vote pour une émotion partagée, pas pour une loi.

**Mise en contexte :** c'est une extension majeure de l'ontologie : elle ne représente pas seulement des préférences, mais aussi des attachements symboliques.

**Mon avis :** à garder pour la vision long terme. Pour le code actuel, cela peut devenir une simple catégorie `symbolic_value` ou `identity_marker`, pas plus.

## Types D'Ontologies

Découpage utile :

- **Ontologie métier** : décrit le domaine d'application, par exemple les vacances.
- **Ontologie de négociation** : décrit le processus commun à toutes les applications.
- **Ontologie politique** : décrit valeurs, récits, identités, désaccords.
- **Ontologie factuelle** : décrit faits, engagements, clauses vérifiables.
- **Ontologie d'interface** : décrit comment présenter les concepts aux utilisateurs non techniques.

## Graphe De Connaissance

Noeuds importants pour Obsidian :

- `Participant`
- `Groupe`
- `Préférence`
- `Contrainte`
- `Veto`
- `Option`
- `Proposition`
- `Concession`
- `Round`
- `Vote`
- `Fitness`
- `Entropie`
- `Accord`
- `Clause`
- `Récit`
- `Valeur`
- `Ontologie`
- `Délégué`

Relations possibles :

- `Participant` appartient à `Groupe`.
- `Participant` exprime `Préférence`.
- `Préférence` concerne `Critère`.
- `Veto` bloque ou pénalise `Option`.
- `Proposition` combine plusieurs `Options`.
- `Round` évalue plusieurs `Propositions`.
- `Accord` contient plusieurs `Clauses`.
- `Récit` justifie ou conteste une `Contrainte`.

## Décisions À Prendre

- Commencer avec une ontologie simple en Python ou directement avec RDF/OWL ?
- Une application peut-elle avoir plusieurs ontologies en parallèle ?
- Quelle partie est stable et quelle partie est modifiable par les utilisateurs ?
- Faut-il versionner l'ontologie ?
- Comment afficher l'ontologie sans perdre les utilisateurs non techniques ?

## À Extraire En Spec

Pour le MVP :

- une liste de classes simples ;
- une liste de relations simples ;
- un mini-graphe de vacances ;
- une fonction qui génère des options valides à partir du graphe.

Pour plus tard :

- une ontologie de négociation générique ;
- une ontologie politique / récit ;
- un format exportable vers Obsidian ou RDF.

## Risque Principal

Faire une ontologie trop ambitieuse, trop abstraite ou trop académique. Le premier objectif est de donner du sens aux options, pas de modéliser toute la société.

