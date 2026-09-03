"""Tests for sentence and word segmentation."""

from __future__ import annotations

from pathlib import Path

import pytest
from nltk.tokenize.punkt import PunktParameters

from sparv.modules.segment.faroese import FAROESE_ABBREVIATIONS, FAROESE_BETTERWORD_CONFIG
from sparv.modules.segment.segment import BetterWordTokenizer, PunktSentenceTokenizer


@pytest.fixture
def faroese_word_tokenizer(tmp_path: Path) -> BetterWordTokenizer:
    """Create a BetterWordTokenizer from the built-in Faroese model.

    Returns:
        A tokenizer configured with the Faroese rules.
    """
    model = tmp_path / "bettertokenizer.fo"
    model.write_text(FAROESE_BETTERWORD_CONFIG, encoding="utf-8")
    return BetterWordTokenizer(model)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("25. mars", ["25.", "mars"]),
        ("Lóg nr. 25.", ["Lóg", "nr.", "25", "."]),
        ("§ 2.", ["§", "2", "."]),
        ("Hetta er t.d. rætt.", ["Hetta", "er", "t.d.", "rætt", "."]),
        ("HB'ari HB’ari HBʼari", ["HB'ari", "HB’ari", "HBʼari"]),
        ("HB-ari B71-fjeppari føroyskt-danskt", ["HB-ari", "B71-fjeppari", "føroyskt-danskt"]),
        ("'orð' – annað", ["'", "orð", "'", "–", "annað"]),
    ],
)
def test_faroese_word_tokenization(
    faroese_word_tokenizer: BetterWordTokenizer,
    text: str,
    expected: list[str],
) -> None:
    """Keep Faroese abbreviations and internal apostrophes/hyphens intact."""
    assert faroese_word_tokenizer.word_tokenize(text) == expected


def test_faroese_abbreviations_prevent_false_sentence_boundaries() -> None:
    """A capitalized word after a known abbreviation must not start a sentence."""
    tokenizer = PunktSentenceTokenizer(PunktParameters(), abbreviations=list(FAROESE_ABBREVIATIONS))

    assert tokenizer.tokenize("Sí t.d. Hetta dømið. Næsta dømi.") == [
        "Sí t.d. Hetta dømið.",
        "Næsta dømi.",
    ]


def test_ordinal_date_does_not_create_sentence_boundary() -> None:
    """Keep an ordinal date inside its sentence while retaining the period."""
    tokenizer = PunktSentenceTokenizer(PunktParameters(), abbreviations=list(FAROESE_ABBREVIATIONS))

    assert tokenizer.tokenize("Fundurin er 25. mars. Næsti fundur er 1. apríl.") == [
        "Fundurin er 25. mars.",
        "Næsti fundur er 1. apríl.",
    ]


def test_longest_abbreviation_is_matched_first(faroese_word_tokenizer: BetterWordTokenizer) -> None:
    """An abbreviation containing periods must win over its shorter prefix."""
    assert faroese_word_tokenizer.word_tokenize("t.d.") == ["t.d."]


def test_maintained_abbreviations_include_final_periods() -> None:
    """Keep the source list readable while normalizing it for the tokenizers."""
    assert "nr." in FAROESE_ABBREVIATIONS
    assert "t.d." in FAROESE_ABBREVIATIONS
    assert all(abbreviation.endswith(".") for abbreviation in FAROESE_ABBREVIATIONS)
    assert "    nr\n" in FAROESE_BETTERWORD_CONFIG
    assert "    t.d\n" in FAROESE_BETTERWORD_CONFIG


def test_short_lived_keep_ordinals_option_is_backward_compatible(tmp_path: Path) -> None:
    """Read a cached intermediate model without restoring its over-broad behavior."""
    model = tmp_path / "cached-bettertokenizer.fo"
    config = FAROESE_BETTERWORD_CONFIG.replace(
        "case_sensitive: false\n",
        "case_sensitive: false\nkeep_ordinals: true\n",
    )
    model.write_text(config, encoding="utf-8")

    assert BetterWordTokenizer(model).word_tokenize("§ 2.") == ["§", "2", "."]
