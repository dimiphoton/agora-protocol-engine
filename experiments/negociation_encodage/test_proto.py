from pathlib import Path

from proto import charger, jouer


HERE = Path(__file__).parent


def test_vacances_tourne() -> None:
    proto = charger(HERE / "vacances.yaml")
    assert proto.anonymat is False
    res = jouer(proto)
    assert res["rounds_joues"] >= 1
    assert res["option_finale"] in {
        "bretagne_gite_voile", "med_hotel_festivals", "bretagne_hotel_voile", "auv_gite_rando",
    }


def test_copropriete_anonyme() -> None:
    proto = charger(HERE / "copropriete.yaml")
    assert proto.anonymat is True
    assert proto.veto_prix > charger(HERE / "vacances.yaml").veto_prix
    res = jouer(proto)
    journal = "\n".join(res["journal"])
    assert "A_rdc" not in journal  # anonymat
    assert "agent_" in journal
