"""Immutable normalized recall notices."""

from dataclasses import dataclass
from datetime import datetime
from dataclasses import field

from .enrichment import RecallDetails


@dataclass(frozen=True, slots=True)
class RecallNotice:
    """A recall notice from an official source, not a product match guarantee."""

    identifier: str
    title: str
    url: str | None
    published: datetime | None
    summary: str
    details: RecallDetails = field(default_factory=RecallDetails)
    source_id: str = "se_food"
