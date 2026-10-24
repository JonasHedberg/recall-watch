"""Asynchronous client for official public recall notices."""

from .client import RecallClient
from .sources import RecallSource, SOURCES, DEFAULT_SOURCE
from .cpsc import parse_cpsc_recalls
from .exceptions import RecallConnectionError, RecallError, RecallHTTPError, RecallParseError
from .models import RecallNotice
from .enrichment import RecallDetails, extract_recall_details
from .matching import matching_notices, parse_keywords
from .parsing import parse_recall_feed
from .serialization import serialize_notice, page_notices, MAX_PREVIEW

__all__ = [
    "RecallClient",
    "RecallSource", "SOURCES", "DEFAULT_SOURCE", "parse_cpsc_recalls",
    "RecallConnectionError",
    "RecallError",
    "RecallHTTPError",
    "RecallNotice",
    "RecallDetails",
    "extract_recall_details",
    "RecallParseError",
    "parse_recall_feed",
    "matching_notices",
    "parse_keywords",
    "serialize_notice",
    "page_notices",
    "MAX_PREVIEW",
]
