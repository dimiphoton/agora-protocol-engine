from proto import exhaustif, least_misery, run_ga, shannon_from_counts


def test_shannon_uniforme() -> None:
    assert abs(shannon_from_counts([1, 1, 1, 1]) - 2.0) < 1e-9


def test_ga_atteint_l_optimum() -> None:
    opt, opt_f = exhaustif()
    best, hist, palier = run_ga(seed=1)
    assert least_misery(best) == opt_f
    assert palier <= hist[-1].gen or palier == hist[-1].gen
    assert opt_f > -50


def test_veto_penalise_camping_pour_p2() -> None:
    from proto import scores_individuels
    sc = scores_individuels(("bretagne", "camping", "velotourisme"))
    assert sc["P2"] < sc["P1"]
