# Synthèse — ce que le brainstorming décrit vraiment

Source : `brainstorming/raw/` (344 échanges Gemini) et `brainstorming/processed/`
(notes interprétatives). Les prototypes A–F sont des *tests* de ces thèses,
pas une réécriture du projet.

## 1. Le projet, sans le pitch

Le dépôt s'appelle `agora-protocol-engine` / « Emergent » dans les échanges.
Ce n'est **pas** une blockchain de paix, **pas** un tableur de votes, **pas**
une DAO qui compte des mains. C'est un **moteur de recherche de compromis
sémantique** : une structure de données qui *représente* un domaine, *sonde*
des participants de façon asynchrone, *infère* des conséquences, *explore*
des packages, et *écrit* un accord à clauses.

Quatre couches, dans l'ordre où le brut les a construites :

1. **Représentation** — ontologie = graphe de classes et de relations
   (`requiert`, `implique`, `incompatible`). Sans ça, le moteur est un
   scoreur aveugle (critique de l'échange 8, acceptée).
2. **Résumé mathématique** — least misery comme métrique de *qualité* d'une
   solution ; entropie `H_cons` comme métrique de *processus* (incertitude,
   où sonder, quand s'arrêter). Ce n'est pas Nash : Nash *analyse* un jeu
   égoïste, le projet *conçoit* un mécanisme vers un optimum social / Pareto.
3. **Recherche** — pas de descente de gradient (espace discret). Exhaustif
   tant que c'est petit ; AG + contraintes dès que ça explose. Le veto n'est
   pas un mur (paradoxe du dictateur, échange 7) : c'est un **coût**.
4. **Règles du jeu encodées, pas hard-codées** — délais, veto, métrique
   (prudence / utilitarisme / enthousiasme), anonymat, rétribution. Un vote
   préliminaire / une méta-négociation choisit le *format* avant le fond
   (échange 323, loi d'Ashby).

La blockchain, quand elle viendra, est un **notaire** : hash de propositions,
engagements, versions d'accord. Le calcul (AG, ontologie, sondage) reste
off-chain. Les tokens `$NEGO` (réputation soulbound) et `$PACT` (dividende)
sont de la vision, pas du core. Gemini a corrigé l'idée d'ICO / grant
Ethereum spéculative.

Le **cas de test fondateur** n'est pas Israël-Palestine. C'est trois
personnes, Bretagne vs Méditerranée, camping vs hôtel, vélo / festivals /
voile (échange 4). Les applications lourdes (paix, UBI, amnistie, gratitude)
sont un backlog explicitement séparé. Le cold start tuerait un protocole
qui n'existe que s'il est adopté par l'ONU.

Profil d'exécution assumé : Python data/scripting, assemblage, pas de
cathédrale RDF ni de Solidity en premier.

## 2. Réponses aux 4 questions (avec les prototypes)

### Q1 — Ontologie unique vs guerre des mots

Le brut a **déjà tranché pour les conflits lourds** (échange 213) : il n'y a
jamais une seule ontologie au départ. Trois temps : ontologies *privées*
(« terroriste » vs « combattant ») → ontologie de *négociation* (bac à sable,
termes-ponts) → ontologie de *consensus* (manuel d'histoire commun, ratifié).
L'échange 214 fige la fédération utile : faits (objectif) / griefs (subjectif
passé) / consensus (avenir).

L'expérience **A** montre que l'unicité *fonctionne* sur le MVP vacances :
taux de mapping 0.93, 13 inférences (`voile` élimine Auvergne, `camping`
implique nature/budget faible), 2 conflits *conceptuels* (camping, festivals).
Un orphelin (`glamping`) signale le bord du lexique, pas un échec.

L'expérience **B** montre le coût de faire semblant que les mots sont communs :
divergence lexicale = 1.00 (aucun label partagé), divergence après
alignement = 0.57, Δ = 0.43. Six guerres résiduelles restent : ce sont des
**préférences opposées sur le même concept**, plus une guerre de vocabulaire.
Les termes-ponts (`hébergement_léger` pour camping/précarité) rendent le
désaccord *dicible* ; ils ne le dissolvent pas.

**Recommandation :** hybride, aligné sur 213, pas sur le rêve d'un graphe
total. Pour le MVP vacances : ontologie de *domaine unique* (A). Dès que les
gens ne se connaissent pas / se détestent (copropriété, budget, paix) :
ontologies privées + table d'alignement + ponts (B). Forcer une ontologie
unique sur un conflit d'identité serait exactement l'oppression que le brut
refuse.

### Q2 — Qui étend l'arbre (maître vs utilisateurs)

L'échange 14 veut du Wikipédia collaboratif et le moins de hard-code possible.
Les notes processed disent : **pas MVP**, ontologie contrôlée d'abord, score
de confiance par relation ensuite.

L'expérience **C** le mesure :

| régime | cohérence | expressivité | contradictions | cycle | produit |
|---|---|---|---|---|---|
| maître | 0.889 | 0.273 | 0 | 0 | 0.242 |
| users libres | 0.812 | 0.909 | 1 | 1 | 0.739 |
| hybride confiance ≥ 0.6 | 0.889 | 0.818 | 0 | 0 | 0.727 |

Le maître seul est sourd (`glamping`, `spa` absents). Les users seuls
cassent le graphe (`glamping is_a camping` *et* `hotel`, cycle bruit↔festivals,
orphelins `karma_vacances`). Le filtre de confiance récupère presque toute
l'expressivité sans les contradictions.

**Recommandation :** le maître (concepteur / bibliothécaire) pose le **tronc**
(classes stables du domaine + ontologie de *négociation* : participant,
proposition, veto, round, clause). Les utilisateurs proposent des branches ;
une relation n'entre que si confiance ≥ seuil et pas de contradiction. C'est
déjà l'idée « ontologie à confiance variable » de l'échange 14.

### Q3 — Liste des MVP sur lesquels se concentrer

Le brut a déjà un backlog (`extensions-sociales.md`) : vacances > colocation
> budget > files d'attente > jeu > paix > gratitude. Les critères de
priorisation y sont : prototypable, explicable, peu de participants, risque
politique faible, données simulables, résultat console, pas de blockchain.

`proto.py` (cette branche) reprend ces critères plus ceux que A–F rendent
mesurables. Classement obtenu :

1. **MVP 0 — script vacances least misery** (échange 4). Déjà l'optimum
   `(Bretagne, Hôtel, Voile)` least_misery=+8, confirmé par l'AG (E, gap=0).
2. **MVP 1 — ontologie de domaine qui infère** (A). Sans ça on a un tableur.
3. **MVP 1b — compteur H_cons + graphe de positions** (D). H=1.04 bits,
   dimension la plus chaude = activité ; un veto sur un quasi-consensus
   *remonte* H (+0.057). C'est le tableau de bord, pas le moteur.
4. **MVP 2 — règles encodées YAML** (F). Vacances : 3 rounds, 1 veto (8 tok),
   1 concession, retour à l'option least misery. Copropriété : anonymat,
   veto 15 tok, 2 vetos, 2 concessions. Le *même* moteur, deux jeux.
5. **MVP 3 — colocation / copropriété travaux.** Même core, gens qui ne
   s'apprécient pas. Test réel de B (guerre des mots légère) et de F
   (anonymat).
6. **MVP 4 — budget collectif.** Plus pitchable, plus de votants, encore
   hors paix.
7. **Plus tard** — AG dès que le génome dépasse ~10³ (E n'est pas nécessaire
   à 36 options) ; ontologie collaborative à confiance ; files d'attente.
8. **Trop tôt** — paix, UBI, amnistie, tokens, on-chain, serious game licencié.

### Q4 — Critères d'utilité et d'efficacité

À ne pas confondre :

| Famille | Question | Proxy mesuré |
|---|---|---|
| Utilité (qualité d'accord) | Personne n'est écrasé ? | least misery ; n conflits conceptuels |
| Efficacité (processus) | On avance ? | ΔH par round/question ; gens jusqu'au palier |
| Coût cognitif | Les gens tiennent ? | n questions, n orphelins, anonymat vs noms |
| Temps à consensus | Combien de rounds ? | rounds jusqu'à H ≤ seuil |
| Robustesse au veto | Un seul peut-il tuer ? | veto=coût ; concession rémunérée ; espace non vide |

L'entropie **n'est pas** l'utilité. H=0 avec least_misery=−20 serait un
consensus *pourri* (tout le monde d'accord que c'est affreux). H mesure
l'incertitude / la dispersion. Le palier d'entropie (E, F) est un
*critère d'arrêt*, pas un trophée.

Le progrès n'est pas monotone (échange 189, confirmé en D) : un grief
nouveau remonte H. Les récompenses devraient tarifer ΔH, y compris les
remontées informatives (découverte), pas seulement les chutes.

## 3. Architecture recommandée (sans Ethereum)

```
ontologie_domaine (maître, tronc)     ← A, C
    + branches users si confiance     ← C
ontologies_privées + ponts            ← B  (activé si divergence lexicale haute)
sondage → notes → H_cons + graphe     ← D
score = least_misery (votable)        ← E, F
veto = prix en tokens internes        ← F, échange 7
arrêt = palier H + fitness            ← E
config YAML = méta-négociation        ← F, échange 323
journal d'événements (liste)          ← place du futur registre on-chain
```

## 4. Trop tôt (ne pas coder)

- Solidity, $PACT, $NEGO, grants Ethereum, forks protocolaires.
- RDF/OWL / Protégé (le brut dit dictionnaires d'abord).
- Paix géopolitique, amnistie, UBI, crédit social (refusé par l'auteur).
- LLM « notaire » qui rédige le contrat : après un mini-langage de clauses.
- Nash comme fonction objectif.

## 5. Limites de ces expériences

Bots, 3 participants, notes inventées (échange 4). Pas d'humains, pas de
fatigue réelle, pas de capture idéologique organisée, pas de spam de
propositions, pas d'asymétrie de pouvoir mesurée. L'AG sur 36 génomes ne
prouve pas le passage à l'échelle. Les termes-ponts de B sont fournis par
l'expérimentateur, pas émergés. C utilise des edits scriptés, pas un wiki
vivant.
