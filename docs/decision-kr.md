# Décision : représentation des connaissances

Décision prise avant le code du core. Une seule pile pour le MVP.

## Besoin réel

Le moteur doit interroger une couche sémantique, pas des chaînes « Bretagne » ou « hôtel » écrites dans le score. Deux graphes :

- **Domaine** : classes, instances, relations. Exemple vacances : `voile` est un sous-type de `nautique`, `voile` requiert `acces_mer`, `festival` implique `budget_eleve`, `randonnee` est incompatible avec `plat`.
- **Négociation** : participant, proposition, round, veto, clause, accord. Indépendant du domaine.

Inférences fermées, pas un web sémantique ouvert :

- hériter une préférence le long de `sous_type` ;
- filtrer ou pénaliser via `requiert` et `incompatible` ;
- propager `implique` (une préférence sur la conséquence s’applique à la cause).

Charge : dizaines à quelques centaines de nœuds, 3 domaines (vacances, resto, weekend), fichiers JSON lisibles par un non-spécialiste et par un script.

## Trois piles

### 1. Graphe RDF + SPARQL (`rdflib`)

Classes, relations et requêtes déclaratives. C’est le format du brainstorming (Protégé, `.owl`).

Pour ce MVP, les règles sont au nombre de quatre et le graphe est petit. SPARQL ajouterait des chaînes de requête difficiles à tester, et le raisonneur RDFS de `rdflib` ne couvre pas nos règles métier (`implique`, veto-coût) sans code Python autour. SPARQL devient pertinent quand l’ontologie est ouverte et écrite par des tiers. Ici il décorerait un moteur qui ferait quand même les inférences en Python.

### 2. JSON-LD seul

Bon format d’échange (types, identifiants). Aucun moteur de requête ni d’inférence. Il faudrait encore NetworkX ou `rdflib` par-dessus. À réserver à un export ultérieur, pas comme pile d’exécution.

### 3. Graphe property (NetworkX) + schéma JSON

Nœuds avec `id` et `type`, arêtes avec `relation`. Scénarios validés par un schéma JSON. Les inférences sont des fonctions Python courtes, testées : `heriter_preferences`, `filtrer_contraintes`, `propager_implique`. Le core appelle `agora/kr/requetes.py`. Changer de domaine = changer le fichier JSON, pas le score.

## Choix

**NetworkX + schéma JSON.**

Raisons : les inférences du domaine vacances sont un jeu fermé ; les requêtes du moteur sont « candidats valides », « préférences étendues », « clauses d’un accord » ; la charge MVP ne justifie pas SPARQL. Le graphe sert vraiment (classes, relations, inférences), la langue de requête reste du Python lisible.

Hors pile : blockchain, scraping, OWL collaboratif.
