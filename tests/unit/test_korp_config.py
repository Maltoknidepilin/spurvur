"""Tests for compact Korp corpus metadata."""

from sparv.modules.korp.config import build_license


def test_build_license_reuses_tei_label_and_target() -> None:
    assert build_license(
        {"fo": "CC BY 4.0", "en": "CC BY 4.0"},
        "https://creativecommons.org/licenses/by/4.0/",
        None,
    ) == {
        "fao": '<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>',
        "eng": '<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>',
    }


def test_build_license_uses_concise_override_for_mixed_rights() -> None:
    result = build_license(
        {"fo": "CC0 1.0"},
        "https://creativecommons.org/publicdomain/zero/1.0/",
        {
            "fao": "Íkast frá [Usable](https://www.usable.dev/) eru latin út undir "
            "[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)."
        },
    )
    assert result == {
        "fao": 'Íkast frá <a href="https://www.usable.dev/">Usable</a> eru latin út undir '
        '<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>.'
    }
