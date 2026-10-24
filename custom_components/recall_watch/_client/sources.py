"""Curated, fixed-endpoint public recall data sources.

Never accept arbitrary URLs from Home Assistant configuration; a compromised
config entry must not permit requests to internal hosts (SSRF prevention).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecallSource:
    """A supported authority and its stable read-only public endpoint."""

    source_id: str
    name: str
    country: str
    category: str
    feed_format: str
    url: str


SOURCES: dict[str, RecallSource] = {
    "eu_safety_gate": RecallSource(
        "eu_safety_gate", "European Union: Safety Gate product alerts", "EU", "consumer", "safety_gate_xml",
        "https://ec.europa.eu/safety-gate-alerts/api/download/weeklyReport/list/xml/en",
    ),
    "se_food": RecallSource(
        "se_food", "Swedish Food Agency", "SE", "food", "rss",
        "https://www.livsmedelsverket.se/rss/rss-aterkallanden",
    ),
    "ca_food": RecallSource(
        "ca_food", "Canada: Food recalls", "CA", "food", "rss",
        "https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls",
    ),
    "ca_consumer": RecallSource(
        "ca_consumer", "Canada: Consumer product recalls", "CA", "consumer", "rss",
        "https://recalls-rappels.canada.ca/en/feed/consumer-products-alerts-recalls",
    ),
    "uk_consumer": RecallSource(
        "uk_consumer", "United Kingdom: Product recalls", "GB", "consumer", "atom",
        "https://www.gov.uk/product-safety-alerts-reports-recalls.atom?product_alert_type%5B%5D=product-recall",
    ),
    "us_consumer": RecallSource(
        "us_consumer", "United States: CPSC recalls", "US", "consumer", "cpsc_json",
        "https://www.saferproducts.gov/restwebservices/Recall?format=json",
    ),
}
DEFAULT_SOURCE = "se_food"
