"""Keyword matching behavior and unsafe-input guards."""

import pytest

from _client import RecallNotice, matching_notices, parse_keywords


def test_no_keywords_match_everything() -> None:
    notices = (RecallNotice("1", "Milk", None, None, ""),)
    assert matching_notices(notices, ()) == notices


def test_swedish_casefold_and_summary_search() -> None:
    notices = (
        RecallNotice("1", "Återkallar Ägg", None, None, "Risk för salmonella"),
        RecallNotice("2", "Cheese recall", None, None, "Other problem"),
    )
    assert matching_notices(notices, parse_keywords("äGG, SALMONELLA")) == (notices[0],)


def test_duplicate_terms_removed() -> None:
    assert parse_keywords("Milk, milk,  , Milk") == ("milk",)


@pytest.mark.parametrize("text", ["a," * 25, "a" * 65, "unsafe\nkeyword"])
def test_invalid_keywords_rejected(text: str) -> None:
    with pytest.raises(ValueError):
        parse_keywords(text)
