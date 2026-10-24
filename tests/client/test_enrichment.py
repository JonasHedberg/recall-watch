"""Deterministic, safety-oriented extraction regression tests."""

import pytest

from _client import extract_recall_details, parse_recall_feed
from _client.serialization import MAX_PREVIEW, page_notices, serialize_notice


def test_explicit_swedish_fields_and_multiple_dates() -> None:
    details = extract_recall_details(
        "Leverantören återkallar chokladkakor på grund av risk för glasfragment",
        "Varumärke: Exempelmat. Batchnummer: AB123, CD456. "
        "Bäst före: 2026-12-30 och 31 december 2026.",
    )
    assert details.product == "chokladkakor"
    assert details.brand == "Exempelmat"
    assert details.risk_type == "foreign_object"
    assert details.batch_numbers == ("AB123", "CD456")
    assert details.best_before_dates == ("2026-12-30", "2026-12-31")


def test_no_brand_assumed_from_recalls_subject() -> None:
    details = extract_recall_details("Arla återkallar proteinpudding", "Risk för glasbitar")
    assert details.product == "proteinpudding"
    assert details.brand is None
    assert details.risk_type == "foreign_object"
    assert details.batch_numbers == ()
    assert details.best_before_dates == ()


def test_unknown_when_facts_not_explicit() -> None:
    result = extract_recall_details("Viktig uppdatering av produkter", "Mer information finns i länken.")
    assert result.product is None
    assert result.brand is None
    assert result.risk_type is None
    assert result.batch_numbers == ()
    assert result.best_before_dates == ()


@pytest.mark.parametrize(("reason", "category"), [
    ("Odeklarerad mjölk", "allergen"),
    ("Risk för listeria", "microbiological"),
    ("För hög halt av kvicksilver", "chemical"),
    ("Produkten har felaktig märkning", "labelling"),
    ("Defekt förpackning", "packaging"),
    ("Glasbitar och salmonella", "multiple"),
])
def test_risk_type_explicit_examples(reason: str, category: str) -> None:
    assert extract_recall_details("Återkallar exempelprodukt", reason).risk_type == category


def test_negation_not_inferred_as_risk() -> None:
    assert extract_recall_details("Provtagning", "Inga spår av listeria hittades.").risk_type is None


def test_explicit_dates_validated_and_normalized() -> None:
    result = extract_recall_details("Återkallar yoghurt", "Sista förbrukningsdag: 31/02/2027; 15.01.2027")
    assert result.best_before_dates == ("2027-01-15",)


def test_batch_not_extracted_without_label_or_from_dates() -> None:
    result = extract_recall_details("Återkallar yoghurt", "Produkten har koden AB123. Bäst före: 2027-02-02")
    assert result.batch_numbers == ()


def test_parser_attaches_enrichment_and_serialization() -> None:
    feed = """<rss><channel><item><guid>ex</guid>
        <title>Butiken återkallar kex på grund av risk för metallbitar</title>
        <description>Varumärke: Exempel. Parti: F0123. Bäst före 2027-03-19.</description>
        </item></channel></rss>""".encode()
    result = parse_recall_feed(feed)
    data = serialize_notice(result[0], include_summary=True)
    assert data["product"] == "kex"
    assert data["brand"] == "Exempel"
    assert data["risk_type"] == "foreign_object"
    assert data["batch_numbers"] == ["F0123"]
    assert data["best_before_dates"] == ["2027-03-19"]
    assert data["summary"]
    assert len(page_notices(result)["notices"]) == 1


def test_unknown_is_none_not_guessed_in_service() -> None:
    result = parse_recall_feed(b"<rss><channel><item><title>Information</title></item></channel></rss>")
    data = serialize_notice(result[0])
    assert data["product"] is None
    assert data["brand"] is None
    assert data["risk_type"] is None
    assert data["batch_numbers"] == []
    assert data["best_before_dates"] == []


def test_paginated_results_and_bounds() -> None:
    xml = '<rss><channel>' + ''.join(f'<item><title>Notice {i}</title></item>' for i in range(15)) + '</channel></rss>'
    notices = parse_recall_feed(xml.encode())
    result = page_notices(notices, offset=10, limit=3)
    assert result["total"] == 15
    assert result["offset"] == 10
    assert result["has_more"] is True
    assert len(result["notices"]) == 3
    assert MAX_PREVIEW <= 10
    for kwargs in ({"offset": -1}, {"limit": 0}, {"limit": 101}, {"offset": 251}):
        with pytest.raises(ValueError):
            page_notices(notices, **kwargs)


def test_declared_milk_is_not_an_undeclared_allergen() -> None:
    assert extract_recall_details("Produktinformation", "Deklarerad mjölk på förpackningen.").risk_type is None


def test_allergen_and_labelling_prefers_specific_allergen() -> None:
    result = extract_recall_details("Återkallar kex", "Odeklarerad mjölk på grund av felaktig märkning")
    assert result.risk_type == "allergen"


def test_malformed_and_ignored_batch_fragments() -> None:
    result = extract_recall_details("Återkallar kex", "Batch: x, 123456789012345678901234567890123, nr, AB12")
    assert result.batch_numbers == ("AB12",)


def test_at_most_five_batches_and_dates() -> None:
    result = extract_recall_details(
        "Återkallar kex", 
        "Batch: A11, A12, A13, A14, A15, A16. "
        "Bäst före: 2027-01-01, 2027-01-02, 2027-01-03, 2027-01-04, 2027-01-05, 2027-01-06",
    )
    assert result.batch_numbers == ("A11", "A12", "A13", "A14", "A15")
    assert result.best_before_dates == (
        "2027-01-01", "2027-01-02", "2027-01-03", "2027-01-04", "2027-01-05",
    )


def test_date_capture_stops_at_new_section() -> None:
    result = extract_recall_details(
        "Återkallar kex", "Bäst före: 2027-05-12! Risk för glasfragment. Batch: AB12"
    )
    assert result.best_before_dates == ("2027-05-12",)
    assert result.batch_numbers == ("AB12",)
