from proto import enumerer_options, evaluer, mapper, Enonce


def test_voile_invalide_en_auvergne() -> None:
    opts = enumerer_options()
    voile_auv = opts[(opts.destination == "auvergne") & (opts.activite == "voile")]
    assert not voile_auv["valide"].any()


def test_voile_valide_en_bretagne() -> None:
    opts = enumerer_options()
    voile_bzh = opts[(opts.destination == "bretagne") & (opts.activite == "voile")]
    assert voile_bzh["valide"].any()


def test_mapping_orphelin() -> None:
    ms = mapper([Enonce("P", "glamping c'est bien", +1)])
    assert ms[0].orphelin


def test_metrics_range() -> None:
    res = evaluer()
    assert 0.7 <= res.metriques["taux_mapping"] <= 1.0
    assert res.metriques["n_options_valides"] < res.metriques["n_options_totales"]
    assert res.metriques["n_conflits_conceptuels"] >= 1
