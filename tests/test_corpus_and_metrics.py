import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from src.corpus import DIGIT_FOR_VOWEL, surface_profile, tokens
from src.evaluation import mcnemar, score, silent_failure_rate


def test_digit_substitution_matches_3_inside_a_word():
    assert DIGIT_FOR_VOWEL.search("slim things de3 wei")
    assert DIGIT_FOR_VOWEL.search("y3di bor bra")


def test_digit_substitution_ignores_standalone_numbers():
    assert not DIGIT_FOR_VOWEL.search("meeting at 3 pm")
    assert not DIGIT_FOR_VOWEL.search("2023 results")


def test_tokens_keep_open_vowels_and_drop_handles_and_urls():
    assert tokens("Yɛyɛ @user https://x.co adwuma") == ["yɛyɛ", "adwuma"]


def test_surface_profile_counts_open_vowel_tokens():
    prof = surface_profile("ampesie bi yɛ guy", english=set())
    assert prof["n_tokens"] == 4
    assert prof["open_vowel_token_share"] == pytest.approx(0.25)


def test_surface_profile_flags_letters_outside_twi_alphabet():
    prof = surface_profile("ceremonial vp nso", english=set())
    assert prof["non_twi_letter_token_share"] == pytest.approx(2 / 3)


def test_silent_failure_rate_counts_only_non_neutral_gold():
    gold = ["positive", "negative", "neutral", "positive"]
    pred = ["neutral", "negative", "neutral", "neutral"]
    assert silent_failure_rate(gold, pred) == pytest.approx(2 / 3)


def test_score_perfect_prediction():
    gold = ["positive", "negative", "neutral"]
    result = score(gold, gold)
    assert result["macro_f1"] == pytest.approx(1.0)
    assert result["silent_failure_rate"] == 0.0


def test_mcnemar_identical_systems_is_not_significant():
    gold = ["positive"] * 10
    assert mcnemar(gold, gold, gold)["p_value"] == 1.0


def test_mcnemar_one_sided_disagreement():
    gold = ["positive"] * 12
    a, b = ["positive"] * 12, ["negative"] * 12
    out = mcnemar(gold, a, b)
    assert out["only_a_correct"] == 12 and out["only_b_correct"] == 0
    assert out["p_value"] < 0.001
