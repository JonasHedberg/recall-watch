"""Deterministic review sampling; no public feed is automatically approved."""
from __future__ import annotations

from _client.enrichment import RecallDetails
from _client.models import RecallNotice
from scripts.live_source_probe import choose_review_samples


def notice(number: int, *, risk: str | None = None, batch: str | None = None) -> RecallNotice:
    return RecallNotice(
        identifier=f"notice-{number}",
        title=f"Original recall {number}",
        url=f"https://authority.example.org/{number}",
        published=None,
        summary="Sample only; needs human comparison",
        details=RecallDetails(risk_type=risk, batch_numbers=(batch,) if batch else ()),
    )


def test_audit_sample_is_diverse_bounded_and_deduplicated() -> None:
    records = tuple(
        notice(n, risk=("fire" if n == 8 else "entrapment" if n == 11 else None),
               batch=("BATCH123" if n == 14 else None))
        for n in range(30)
    )
    samples = choose_review_samples(records)
    ids = [item.identifier for item in samples]
    assert len(ids) == len(set(ids))
    assert len(ids) <= 12
    assert {"notice-0", "notice-1", "notice-28", "notice-29",
            "notice-8", "notice-11", "notice-14"}.issubset(ids)


def test_audit_sampling_small_sources_and_empty_sources() -> None:
    assert choose_review_samples(()) == []
    records = (notice(0), notice(1), notice(2))
    assert [n.identifier for n in choose_review_samples(records)] == [
        "notice-0", "notice-1", "notice-2"
    ]
