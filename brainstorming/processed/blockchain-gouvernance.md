# Blockchain & Gouvernance

Source brute : `brainstorming/raw/gemini-ontologie-pour-la-recherche-de-compromis.md`

Ce fichier regroupe les échanges sur la blockchain, les tokens, la gouvernance, la légitimité, la réputation et les engagements publics.

## Map Of Content

- [But du Bloc](#but-du-bloc)
- [Échanges À Relire](#échanges-à-relire)
- [Sous-Blocs](#sous-blocs)
- [Fiches D'Échanges](#fiches-déchanges)
- [On-Chain Ou Off-Chain](#on-chain-ou-off-chain)
- [Objets De Gouvernance](#objets-de-gouvernance)
- [Décisions À Prendre](#décisions-à-prendre)
- [À Extraire En Architecture](#à-extraire-en-architecture)

## But Du Bloc

La blockchain ne doit pas être le point de départ du MVP.

Elle devient intéressante pour :

- rendre visibles les engagements ;
- conserver une mémoire publique ;
- auditer les décisions ;
- légitimer un processus distribué ;
- gérer des tokens, récompenses ou réputations ;
- éviter qu'un acteur central efface ou réécrive le processus.

## Échanges À Relire

| Lien brut | Question abrégée | Réponse abrégée |
|---|---|---|
| [Échange 18](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-18) | Imaginer d'autres rôles : votant, délégué, explorateur, affineur. | Extension de la gouvernance : contributions multiples au processus, pas seulement votes. |
| [Échange 19](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-19) | Ajouter actions comme baisser exigences ou sous-négocier. | La négociation devient un ensemble d'actions reconnues et potentiellement récompensées. |
| [Échange 61](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-61) | Les médias pourraient interroger la blockchain pour comprendre un conflit. | La blockchain sert de mémoire publique lisible, pas seulement de registre financier. |
| [Échange 63](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-63) | Équivalents du minage, staking, ICA dans cette application. | Transposition des mécanismes crypto vers preuve d'effort de négociation et réputation. |
| [Échange 67](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-67) | Tokeniser l'avenir est fragile sans État de droit. | La blockchain ne suffit pas ; besoin de garanties, arbitrage et conditions d'exécution. |
| [Échange 76](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-76) | La communication ne doit jamais être coupée entre les humains. | La blockchain peut maintenir un canal et une mémoire, mais pas remplacer la discussion. |
| [Échange 77](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-77) | Faut-il héberger ontologie, sondage, résultats et décisions on-chain ? | Non pour le calcul lourd ; on-chain pour preuves, états, engagements et audit. |
| [Échange 82](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-82) | Que récupèrent les citoyens éloignés qui achètent des tokens ? | Début d'une réflexion sur incitations, dividendes, réputation et soutien externe. |
| [Échange 88](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-88) | Qui peut abonder en $PACT et combien ? | Exploration du financement par crowdfunding, institutions, fonds et acteurs publics. |
| [Échange 103](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-103) | Empêcher les geeks de spammer toutes les propositions. | Coûts, filtres, réputation ou délégation pour éviter l'abus de participation. |
| [Échange 104](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-104) | Pourquoi la recherche de solutions ne peut-elle pas être hébergée sur blockchain ? | Calcul trop coûteux et inefficace ; préférer off-chain + preuves ou journalisation. |
| [Échange 109](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-109) | Fitness par rounds de vote, récompense de participation et accommodation. | La blockchain peut enregistrer votes, efforts et récompenses, mais pas décider seule. |
| [Échange 130](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-130) | Prendre en compte les forks. | Le fork devient un mécanisme de sortie, pluralité ou protection contre capture. |
| [Échange 178](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-178) | Les grants Ethereum financent-elles ce type d'idée ? | Orientation vers infrastructure, civic tech et utilité publique plutôt que tokenomics. |
| [Échange 284](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-284) | Quel serait l'équivalent d'un pool de minage ? | Transposition vers pool de contributeurs, validateurs ou chercheurs de compromis. |
| [Échange 316](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-316) | ONU ou clandestinité pour une négociation démocratique ? | Exploration des sources de légitimité : institution, peuple, preuve, adoption. |
| [Échange 339](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-339) | Contacter P2P Foundation sur une blockchain de négociation de conflit. | Reformulation vers communs, reconnaissance des valeurs et sortie citoyenne des blocages. |
| [Échange 340](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-340) | Ajouter permanence, masse, récits, récompense de la négociation. | Les quatre piliers deviennent mémoire, pluralité ontologique, légitimité, incitation. |

## Sous-Blocs

### 1. Mémoire Et Permanence

La blockchain est envisagée comme une mémoire :

- des propositions ;
- des votes ;
- des engagements ;
- des versions d'accord ;
- des preuves de participation ;
- des validations collectives.

Elle sert surtout à empêcher l'effacement ou la réécriture arbitraire.

### 2. Rôles De Gouvernance

Rôles évoqués :

- votant ;
- délégué ;
- explorateur de solutions ;
- affineur de frontières ;
- validateur ;
- avocat ;
- arbitre ;
- contributeur d'ontologie ;
- participant externe.

Le projet ne doit pas seulement demander “qui vote ?”, mais “qui aide le processus à progresser ?”.

### 3. Tokens Et Récompenses

Tokens évoqués :

- `$NEGO` : réputation, effort de négociation, signal non purement financier.
- `$PACT` : dividende, engagement, matérialisation d'un gain de paix.
- tokens de gratitude : reconnaissance d'externalités positives.

À garder en tête : les tokens ne doivent pas devenir le coeur spéculatif du projet.

### 4. Calcul Off-Chain

Un point important : le calcul lourd ne doit probablement pas être fait on-chain.

Raisons :

- coût ;
- lenteur ;
- complexité ;
- consommation ;
- confidentialité ;
- évolutivité.

La blockchain peut stocker les preuves, les résultats, les engagements et les états importants, pas toute la recherche.

### 5. Légitimité Et Adoption

La blockchain peut aider si elle sert :

- la transparence ;
- la continuité ;
- l'auditabilité ;
- la participation massive ;
- la coexistence de récits.

Elle nuit au projet si elle donne une impression de gadget crypto ou de solution imposée aux gens.

### 6. Forks Et Non-Interférence

Les forks apparaissent comme un mécanisme ambivalent :

- protection contre capture ;
- risque de fragmentation ;
- possibilité de pluralité ;
- problème des fonds et de la légitimité.

La non-interférence est importante pour les acteurs extérieurs : aider sans confisquer le conflit.

## Fiches D'Échanges

### Échanges 18-20 - Rôles Et Actions

Liens bruts : [Échange 18](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-18), [Échange 19](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-19), [Échange 20](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-20)

**Tes questions (verbatim) :**

> il y a peut-être d'autres actions , rôles (votant, délégué, explorateur de solution, affineur de frontières) auquels je n'ai pas pensé. Libère-toi et propose des rôles. Aussi, puisqu'on a quelque chose qui ressemble à de l'exploration (générations?) , qu'est-ce qui tient lieu d'exploitation?

> ajoute d'autres actions ou rôles. par exemple baisser ces exigences. ou alors faire une sous-négociation avec son groupe opposé (parfois on se rend compte que l'entente est possible). Par contre vendre son vote je trouverai ca bizarre. Aussi, que penses-tu d'un mécanisme de pari (ou de edge).

**Ce que tu cherches :** tu veux dépasser les rôles passifs et inventer des rôles actifs (explorateur, affineur de frontières, baisse d'exigence, sous-négociation). Tu poses aussi l'analogie exploration/exploitation, et tu poses une limite morale : pas de vente de vote.

**Réponse Gemini :** Gemini propose que chaque *fonction* du système devienne un *rôle* incité économiquement, avec un type de « preuve » associé : le **Bibliothécaire** (propose concepts/relations dans l'ontologie → Proof-of-Knowledge), le **Vérificateur** (vote la qualité du « vrai » → Proof-of-Consensus), le **Mutateur** (ton « affineur de frontières » : améliore une solution, payé *au prorata du gain de score* → Proof-of-Improvement), et l'**Arbitre** (ton « délégué » élu, déclenche des votes sur les règles → Proof-of-Governance). Il répond aussi à ta question exploration/exploitation : l'exploration trouve les idées, l'exploitation (le Mutateur) les affine.

**Mise en contexte :** c'est la naissance de la gouvernance du protocole. Le système ne doit pas seulement agréger des préférences, il doit reconnaître des contributions différentes au processus.

**Mon avis :** c'est important pour plus tard, mais le MVP doit rester simple. Les premiers rôles peuvent être seulement `participant` et `facilitator`.

### Échanges 76-79 - Tout Mettre Sur La Blockchain ?

Liens bruts : [Échange 76](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-76), [Échange 77](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-77), [Échange 79](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-79)

**Tes questions (verbatim) :**

> tiens il y a une caractéristique de mon projet: la communication n'est jamais coupée entre les hommes au contraire de la guerre. C'était l'idée de départ d'héberger l'IA sur une blockchain. qu'as-tu à proposer?

> tu dit que l'IA (AG/Solver) n'est pas sur la blockchain. explique. Je pensais héberger l'ontologie, le programme de sondage, les résultats, et la prise de décision tout sur la blockchain

**Ce que tu cherches :** tu rappelles l'intuition fondatrice (la communication n'est jamais coupée, d'où la blockchain), et tu contestes le fait que l'IA soit hors-chaîne. Tu voulais tout mettre on-chain : ontologie, sondage, résultats, décision.

**Réponse Gemini :** Gemini te dit que tu as *philosophiquement* raison (la logique est ancrée sur la chaîne) mais *techniquement* tort de croire que l'IA y est hébergée : la blockchain est « stupide, lente et chère », conçue pour être un **juge de paix incorruptible**, pas un cerveau rapide. Son analogie : le **Bureau d'Architecte** (off-chain) où l'IA explore des millions de plans, vite et pas cher (ton script Python), vs le **Notaire** (on-chain) qui ne calcule rien mais vérifie, tamponne et conserve le plan final, de façon lente, chère et digne de confiance. D'où une architecture à trois niveaux (exécution off-chain, registre on-chain, interface).

**Mise en contexte :** c'est un pivot architectural essentiel. La blockchain n'est pas l'ordinateur principal du projet.

**Mon avis :** très bonne clarification. Pour le repo actuel, il faut coder comme si tout était off-chain. Plus tard, on pourra journaliser certains événements.

### Échanges 82-90 - $PACT, $NEGO Et Financement Externe

Liens bruts : [Échange 82](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-82), [Échange 85](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-85), [Échange 88](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-88), [Échange 90](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-90)

**Tes questions (verbatim) :**

> question bête: que récupèrent les citoyens non impliqués qui ont acheté des tokens?

> plus précisément, essaie de me faire une idée de qui peux abonder en $PACT et surtout combien . je sais que le crowdfunding peut atteindre des sommets mais je n'ai pas de connaissances financières pour le comparer à des bonds, contrats d'assurance, hedge funds

**Ce que tu cherches :** tu testes la couche économique : que gagne un détenteur de tokens non impliqué dans le conflit, et qui pourrait abonder en $PACT et à quelle échelle (comparé à bonds, assurances, hedge funds). Tu reconnais ton manque de bagage financier.

**Réponse Gemini :** Gemini dit que ta question n'est pas bête : c'est ce qui distingue ton projet d'une charité. Un étranger qui achète un token n'est pas un donateur mais un **investisseur d'impact** dont le retour dépend du *succès*, pas du *hype*. Il pose le **double jeton** : les participants gagnent du **$NEGO** (réputation, non transférable, « soulbound »), les investisseurs achètent du **$PACT** (financier, transférable). Et il décrit le « contrat d'investissement de paix » : l'argent finance la trésorerie de négociation ; si la paix est signée, le Dividende promis (ex. 500M€ par l'ONU/Banque Mondiale) **rembourse d'abord les investisseurs** avant de distribuer un revenu de base.

**Mise en contexte :** ce passage construit la couche économique du protocole.

**Mon avis :** intéressant mais dangereux pour la crédibilité. À ne pas mettre dans le MVP. À formuler plus tard comme “mécanismes d'incitation”, pas comme promesse financière.

### Échanges 100-109 - Propositions Et Calcul Off-Chain

Liens bruts : [Échange 103](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-103), [Échange 104](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-104), [Échange 109](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-109)

**Tes questions (verbatim) :**

> il faudrait penser à ne pas laisser les geeks spammer toutes les propositions possibles et imaginables.

> fais un calcul d'ordre de grandeur et dis-moi pourquoi la recherche de solutions ne peut pas être héberger sur la blockchain. Je comprends pour le sondage, mais pas pour le parcours de l'ontologie

> pour moi le calcul de la fitness se ferait par des rounds de vote, avec récompense de participation et d'effort d'accomodation. d'ailleurs, comment la blockchain pourrait-elle faire autrement?

**Ce que tu cherches :** tu veux empêcher le spam de propositions, comprendre par un ordre de grandeur pourquoi la recherche de solutions ne tient pas on-chain, et tu proposes que la fitness se calcule par des rounds de vote récompensés plutôt que par un calcul lourd.

**Réponse Gemini :** Gemini fait le **calcul d'ordre de grandeur** que tu demandais : évaluer une fitness `least misery` ≈ 100 000 gas, et un AG a besoin d'évaluer ~100 000 solutions → ~10 milliards de gas, soit ≈100 ETH ≈ 250 000 € pour *un seul* cycle d'optimisation. Conclusion : la blockchain est « prohibitivement coûteuse » pour le calcul intensif. Le parcours de l'ontologie est exclu de la chaîne pour la même raison, plus le coût de stockage des données sémantiques. Donc génération de solutions et calcul **off-chain**, et seulement les preuves/résultats publiés on-chain. Cela rejoint ta proposition (échange 109) : la « fitness » calculée par des rounds de vote récompensés.

**Mise en contexte :** c'est la partie la plus concrète pour une architecture blockchain réaliste.

**Mon avis :** c'est exactement la bonne séparation : `core` en Python d'abord, puis `registry` plus tard. Il faut éviter de commencer par Solidity.

### Échanges 130-132 - Forks

Liens bruts : [Échange 130](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-130), [Échange 131](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-131), [Échange 132](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-132)

**Ta question (verbatim) :**

> Ah oui tiens. Je n'ai pas pensé aux forks

**Ce que tu cherches :** tu découvres la question des forks et tu l'adoptes comme une dimension à part entière de la gouvernance. C'est une ouverture courte mais qui fait basculer la discussion vers le désaccord-comme-branche.

**Réponse Gemini :** Gemini te met en garde : un fork ici est « 100 fois plus dangereux », c'est une **guerre civile protocolaire**. Il déroule le scénario catastrophe : un groupe de durs copie le code (AGPL, c'est légal) et lance « Emergent-A » concurrent. Conséquences : **division de la liquidité $PACT** (les bailleurs ne savent plus où envoyer les fonds), **division de la légitimité** (la population ne sait plus quel protocole est « le vrai »), et surtout **guerre sémantique totale** — deux « manuels d'histoire » concurrents et immuables sur la chaîne, chacun prouvant que l'autre a tort : on a numérisé et financé le schisme. Il propose ensuite des garde-fous de gouvernance.

**Mise en contexte :** c'est une idée propre aux protocoles décentralisés : le désaccord peut créer une branche plutôt qu'un blocage.

**Mon avis :** à garder pour la couche blockchain, mais pas pour le MVP. Dans le core, l'équivalent simple serait “copier un scénario et tester une autre règle”.

### Échanges 178-190 - Ethereum Grants

Liens bruts : [Échange 178](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-178), [Échange 180](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-180), [Échange 185](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-185), [Échange 190](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-190)

**Ta question (verbatim) :**

> fais une recherche sur les grant ethereum. est-ce qu'elles finances des idées de blockchain utilisant ethereum ou des amélioration d'ethereum lui-même?

**Ce que tu cherches :** tu veux savoir si les grants Ethereum financent des applications qui utilisent Ethereum (comme la tienne) ou seulement des améliorations du protocole lui-même. C'est une question de positionnement pour ton financement.

**Réponse Gemini :** Gemini te pousse à pitcher l'infrastructure, pas la tokenomie, et à comprendre les attentes de l'écosystème Ethereum.

**Mise en contexte :** ce passage relie blockchain et stratégie de financement.

**Mon avis :** réaliste : une grant Ethereum serait plus crédible si tu montres un outil public, modulaire, non spéculatif, avec un prototype clair.

### Échanges 313-320 - Légitimité Et Non-Interférence

Liens bruts : [Échange 313](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-313), [Échange 316](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-316), [Échange 319](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-319), [Échange 320](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-320)

**Ta question (verbatim) :**

> Question pour la négociation de fin de conflit. On a evoqué deux solutions pour que la négociation soit démocratique : soit appuyée par l'Onu, soit clandestine. Il faudrait encoder dans l'IA une recompense collective à la participation du plus grand nombre

**Ce que tu cherches :** tu opposes deux voies de légitimité (appui de l'ONU vs processus clandestin) et tu proposes une solution propre au protocole : une récompense collective qui incite à la participation massive comme source de légitimité.

**Réponse Gemini :** Gemini transforme ton idée en **« Loi de Metcalfe » appliquée à la paix** : plus il y a de participants, plus la valeur du réseau (et la récompense individuelle) croît, faisant passer le projet d'un groupe « élitiste » à une « réalité incontournable ». Il code une **« prime à la masse critique »** via un Smart Contract de trésorerie à **paliers de participation** : 1 000 participants → 100k$, 10 000 → 2M$, 100 000 → 50M$, majorité de la population → 1Md$ (« Plan Marshall »). L'effet de nudge : Jean voit « si tu inscris ton voisin, la valeur de TON ticket augmente de 50 € » — la viralité est encodée dans l'incitation financière.

**Mise en contexte :** ce bloc montre que la gouvernance n'est pas seulement technique. Elle touche à la souveraineté du processus.

**Mon avis :** essentiel pour la vision paix, mais il faut d'abord prouver que le moteur peut aider une petite négociation.

### Échanges 339-341 - Formulation P2P

Liens bruts : [Échange 339](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-339), [Échange 340](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-340), [Échange 341](../raw/gemini-ontologie-pour-la-recherche-de-compromis.md#échange-341)

**Tes questions (verbatim) :**

> Trouve le bon interlocuteur et ecris un court mail qui decris mon souhait de prototyper une blockchain de negociation de conflit, tournée vers la reconnaissance des valeurs, des communs... et qui permettrait une sortie citoyenne des blocages

> Réeécris le pour ajouter ce qui m'intéresse: la permanence de la blockchain, la legitimité par la masse, la reconnaissance des différents recits (ontologies) et la récompense de la négociation cobtre le cynisme. Comme c'est un protocole, il pourrait s'appliquer à differents cas: gouvernance de ville, conflits,...

**Ce que tu cherches :** tu condenses ta vision pour un interlocuteur P2P : blockchain de négociation, reconnaissance des valeurs et des communs, sortie citoyenne des blocages, permanence, légitimité de masse, reconnaissance de récits multiples, récompense de la négociation contre le cynisme, et applicabilité générale (ville, conflits).

**Réponse Gemini :** Gemini identifie l'interlocuteur idéal : **Michel Bauwens**, fondateur de la P2P Foundation, belge, accessible, théoricien du passage de l'État-Nation à l'« État-Partenaire ». Il rédige un email qui présente « Emergent » comme une architecture (blockchain + IA) faisant de la résolution de conflits un **« Commun Numérique »**, avec l'hypothèse d'une sortie de crise *par le bas* (stigmergie, réputation) là où l'État et le marché échouent. Point clé qu'il insère : ne pas demander de financement mais une **validation théorique**, pour ancrer le projet dans la philosophie des Communs et éviter la dérive technocratique.

**Mise en contexte :** c'est le meilleur passage pour transformer la blockchain en langage politique plutôt qu'en jargon crypto.

**Mon avis :** à reprendre pour le README long terme. Mais le README du code doit rester plus sobre : “moteur expérimental de compromis sémantique”.

## On-Chain Ou Off-Chain

### À Mettre Plutôt On-Chain

- hash d'une proposition ;
- validation d'un round ;
- version d'un accord ;
- preuve de participation ;
- engagement signé ;
- distribution de récompense ;
- historique minimal auditable.

### À Garder Plutôt Off-Chain

- génération de candidats ;
- calcul d'optimisation ;
- modèles IA ;
- détails sensibles ;
- brouillons ;
- simulations ;
- données personnelles.

## Objets De Gouvernance

- `Proposal`
- `Vote`
- `Delegation`
- `Round`
- `Reputation`
- `Commitment`
- `AgreementVersion`
- `Reward`
- `Fork`
- `AuditTrail`

## Décisions À Prendre

- Faut-il d'abord une version sans blockchain ? Oui, probablement.
- La blockchain sert-elle au MVP vacances ? Non.
- La blockchain sert-elle au pitch long terme ? Oui.
- Les tokens sont-ils nécessaires au premier prototype ? Non.
- Quelle blockchain viser plus tard ? Ethereum peut être pertinent pour les grants, mais pas pour démarrer le core.

## À Extraire En Architecture

- Un schéma `off-chain core / on-chain registry`.
- Une liste des événements à journaliser.
- Une version sans token.
- Une version avec réputation.
- Une version très future avec dividende ou gratitude.

## Risque Principal

Transformer un moteur de médiation en projet crypto spéculatif. La blockchain doit servir la confiance et la mémoire, pas manger le projet.

