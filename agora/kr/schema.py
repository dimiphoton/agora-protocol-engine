"""Schéma JSON d'un scénario de négociation.

Un scénario décrit un domaine (dimensions, nœuds, relations) et les
participants. Il ne contient pas les notes : elles arrivent à part.
"""

SCHEMA_SCENARIO: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ScenarioAgora",
    "type": "object",
    "required": [
        "id",
        "domaine",
        "dimensions",
        "noeuds",
        "relations",
        "participants",
    ],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "domaine": {"type": "string", "minLength": 1},
        "dimensions": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "noeuds": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "type", "label"],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "type": {"type": "string", "minLength": 1},
                    "label": {"type": "string"},
                    "traits": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source", "relation", "cible"],
                "properties": {
                    "source": {"type": "string", "minLength": 1},
                    "relation": {"type": "string", "minLength": 1},
                    "cible": {"type": "string", "minLength": 1},
                },
            },
        },
        "participants": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "label"],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "label": {"type": "string"},
                },
            },
        },
    },
}
