from proto import ENONCES_COUVERTURE, contradictions, has_cycle, regime_maitre, regime_users


def test_maitre_plus_coherent() -> None:
    racines = {"destination", "logement", "activite"}
    m = regime_maitre().metriques(racines, ENONCES_COUVERTURE)
    u = regime_users().metriques(racines, ENONCES_COUVERTURE)
    assert m["coherence"] > u["coherence"]
    assert u["expressivite"] > m["expressivite"]


def test_users_ont_des_bugs() -> None:
    u = regime_users()
    assert contradictions(u.relations)
    assert has_cycle(u.relations)


def test_maitre_sans_cycle() -> None:
    assert not has_cycle(regime_maitre().relations)
