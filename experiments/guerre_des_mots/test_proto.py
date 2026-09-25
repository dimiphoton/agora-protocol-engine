from proto import ALIGNEMENT, divergence_alignee, divergence_lexicale, evaluer, Parti, ONTO_P1, ONTO_P2


def test_lexicale_plus_haute_que_alignee() -> None:
    partis = [Parti("a", ONTO_P1), Parti("b", ONTO_P2)]
    assert divergence_lexicale(partis) > divergence_alignee(partis)


def test_tout_label_aligne() -> None:
    m, _, guerres = evaluer()
    assert m["taux_alignement_labels"] == 1.0
    assert m["n_guerres_residuelles"] >= 1
    assert set(guerres["concept"]).issubset(set(ALIGNEMENT.values()))


def test_delta_positif() -> None:
    m, _, _ = evaluer()
    assert m["delta_divergence"] > 0.3
