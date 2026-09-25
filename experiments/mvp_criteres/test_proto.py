from proto import CRITERES, tableau


def test_huit_criteres() -> None:
    assert len(CRITERES) == 8


def test_vacances_devant_paix() -> None:
    df = tableau().set_index("mvp")
    assert df.loc["0_vacances_least_misery", "total"] > df.loc["9_paix_onchain", "total"]
    assert df.loc["1_ontologie_domaine", "total"] > df.loc["5_ontologie_collaborative", "total"]


def test_yaml_meilleure_robustesse_veto() -> None:
    df = tableau().set_index("mvp")
    assert df.loc["2_regles_yaml", "robustesse_veto"] > df.loc["0_vacances_least_misery", "robustesse_veto"]
