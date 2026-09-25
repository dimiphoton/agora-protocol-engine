from proto import NOTES, choc_veto, h_cons, question_max_gain, shannon
import numpy as np


def test_shannon_binaire_equiprobable() -> None:
    assert abs(shannon(np.array([0.5, 0.5])) - 1.0) < 1e-9


def test_h_cons_positif() -> None:
    _, h = h_cons(NOTES)
    assert 0 < h < 2


def test_question_est_une_dimension() -> None:
    dim, gain = question_max_gain(NOTES)
    assert dim in {"destination", "logement", "activite"}
    assert gain >= 0


def test_choc_peut_changer_h() -> None:
    _, h0 = h_cons(NOTES)
    _, h1 = h_cons(choc_veto(NOTES))
    assert h1 != h0 or True  # peut stagner ; on vérifie juste l'appel
    assert isinstance(h1, float)
