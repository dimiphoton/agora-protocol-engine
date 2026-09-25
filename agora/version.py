"""Version git affichée par le CLI et l'interface."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_RACINE = Path(__file__).resolve().parents[1]


def version_git() -> str:
    """Sha ou description git, sinon ``AGORA_GIT_SHA``, sinon ``inconnue``.

    On n'invente pas de sha : seule la sortie de git ou la variable
    d'environnement est renvoyée.
    """
    decrit = _git("describe", "--tags", "--always", "--dirty")
    if decrit:
        return decrit
    court = _git("rev-parse", "--short", "HEAD")
    if court:
        return court
    environnement = os.environ.get("AGORA_GIT_SHA", "").strip()
    if environnement:
        return environnement
    return "inconnue"


def _git(*args: str) -> str | None:
    try:
        processus = subprocess.run(
            ["git", *args],
            cwd=_RACINE,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if processus.returncode != 0:
        return None
    texte = (processus.stdout or "").strip()
    return texte or None
