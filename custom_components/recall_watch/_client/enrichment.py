"""Conservative, deterministic extraction of facts explicit in recall notice text.

The source is unstructured. Missing fields remain None / empty: there is no
brand inference from a recalling company's name and no fabricated batch match.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

MAX_TEXT = 4096
MAX_CAPTURE = 120
MAX_ITEMS = 5


@dataclass(frozen=True, slots=True)
class RecallDetails:
    """Best-effort fields, never evidence of an affected product or batch."""

    product: str | None = None
    brand: str | None = None
    risk_type: str | None = None
    batch_numbers: tuple[str, ...] = ()
    best_before_dates: tuple[str, ...] = ()


_PRODUCT = re.compile(
    r"(?:\båterkallar\s+|\båterkallelse\s+av\s+|\brecalls\s+)"
    r"(?P<value>[^.!?\n]{2,180})",
    re.IGNORECASE,
)
_UK_RECALL_TITLE = re.compile(
    r"^Product Recall:\s*(?P<product>.+?)(?:\s*\(\d{4}-\d{4}\))?\s*$", re.I
)
_CANADA_RECALL_TITLE = re.compile(
    r"^(?P<product>.+?)\s+recalled\s+due\s+to\b", re.I
)
_PRODUCT_END = re.compile(
    r"\s+(?:på grund av|p\.?g\.?a\.?|efter att|då (?:den|det|de)|som kan|"
    r"kan\s+innehålla|då\s+produkterna?\s+kan|may\s+contain|can\s+contain|"
    r"eftersom|till följd av|due to|because of|for possible|after discovering|risk för)\b",
    re.IGNORECASE,
)
_BRAND = re.compile(
    r"\b(?:(?:varumärke|varumärket|brand(?:\s+name)?)\s*:\s*|"
    r"(?:av märket|märket)\s+)"
    r"(?P<value>[\wÅÄÖåäö][\wÅÄÖåäö&'\- ]{1,65})",
    re.IGNORECASE,
)
_BRAND_END = re.compile(
    r"\s+(?:med|och|som|på grund av|p\.?g\.?a\.?|då|eftersom|har|återkallas|"
    r"återkallar|risk för|kan innehålla|innehåller|due to|because)\b",
    re.IGNORECASE,
)
_BATCH_LABEL = re.compile(
    r"\b(?:batch(?:nummer|nr)?|parti(?:nummer|nr)?|lot(?:nummer|nr)?)"
    r"\s*(?:nr\.?|number|no\.?)?\s*[:#]?\s*"
    r"(?P<values>[A-Za-zÅÄÖåäö0-9][A-Za-zÅÄÖåäö0-9,; /\-]{1,115})",
    re.IGNORECASE,
)
_BATCH_STOP = re.compile(
    r"\b(?:bäst\s+före|best\s+before|sista\s+förbrukningsdag|"
    r"på grund av|risk för|orsaken|återkallas|återkallar|förpackning)\b",
    re.IGNORECASE,
)
_BATCH_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,31}$")
_DATE_LABEL = re.compile(
    r"\b(?:bäst[\s-]*före(?:[\s-]*datum)?|sista\s+förbrukningsdag(?:en)?|"
    r"best\s+before|use\s+by)\s*(?::|är|den|till|datum)?\s*",
    re.IGNORECASE,
)
_DATE_TOKEN = re.compile(
    r"(?<![\d])(?:20\d{2}[-./]\d{1,2}[-./]\d{1,2}|"
    r"\d{1,2}[-./]\d{1,2}[-./]20\d{2}|"
    r"\d{1,2}\s+(?:januari|februari|mars|april|maj|juni|juli|augusti|"
    r"september|oktober|november|december)\s+20\d{2})(?!\d)",
    re.IGNORECASE,
)
_MONTHS = {month: n for n, month in enumerate(
    ("januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"), 1
)}

_RISK_PATTERNS: dict[str, re.Pattern[str]] = {
    "allergen": re.compile(
        r"\b(?:odeklarerad(?:e|t)?\s+allergen(?:er)?|odeklarerad(?:e|t)?\s+"
        r"(?:mjölk|ägg|nötter|gluten|soja|jordnötter)|felaktig\s+allergenmärkning|"
        r"allergen(?:er)?\s+(?:saknas|inte\s+deklarerad)|"
        r"risk\s+för\s+allergisk\s+reaktion|undeclared\s+allergen(?:s)?|"
        r"undeclared\s+(?:egg|soy|sesame|milk|peanuts?|wheat|gluten|nuts?))\b", re.I
    ),
    "foreign_object": re.compile(
        r"\b(?:glasfragment|glasbitar|metallfragment|metallbitar|plastfragment|"
        r"plastbitar|främmande\s+föremål|foreign\s+object|"
        r"pieces\s+of\s+(?:glass|metal|plastic))\b", re.I
    ),
    "microbiological": re.compile(
        r"\b(?:salmonella|listeria(?:\s+monocytogenes)?|campylobacter|"
        r"norovirus|e\.?\s*coli|escherichia\s+coli)\b", re.I
    ),
    "chemical": re.compile(
        r"\b(?:kvicksilver|kadmium|blyhalt|för\s+hög\s+halt\s+av\s+bly|"
        r"pesticid(?:er)?|bekämpningsmedel|aflatoxin|ochratoxin|mercury|cadmium)\b", re.I
    ),
    "labelling": re.compile(
        r"\b(?:felmärkning|felmärkt(?:a)?|felaktig\s+märkning|"
        r"incorrect(?:ly)?\s+labell?ing|mislabelled)\b", re.I
    ),
    "fire": re.compile(r"\b(?:fire\s+(?:and\s+burn\s+)?hazards?|risk\s+of\s+fire|brandrisk)\b", re.I),
    "burn": re.compile(r"\b(?:burn\s+hazards?|risk\s+of\s+burns|brännskador)\b", re.I),
    "electric_shock": re.compile(r"\b(?:electric\s+shock|electrocution|elektrisk\s+stöt)\b", re.I),
    "choking": re.compile(r"\b(?:choking\s+hazard|kvävningsrisk)\b", re.I),
    "fall": re.compile(r"\b(?:fall\s+hazard|fallrisk|risk\s+of\s+falling)\b", re.I),
    "packaging": re.compile(
        r"\b(?:defekt\s+förpackning|felaktig\s+förpackning|"
        r"skadad\s+förpackning|defective\s+packaging)\b", re.I
    ),
}
_NEGATION = re.compile(
    r"\b(?:ingen|inget|inga|utan|negativt\s+för|fri(?:tt)?\s+från|"
    r"no|without|negative\s+for|free\s+from)\b", re.I
)


def _clean(value: str) -> str | None:
    """Keep short meaningful text, not markup or trailing separators."""
    result = value.strip(" :;,.-—–\t\n\r")
    return result[:MAX_CAPTURE] if len(result) >= 2 else None


def _product(title: str) -> str | None:
    """Parse only explicitly marked product headlines, without company inference."""
    uk = _UK_RECALL_TITLE.fullmatch(title)
    if uk:
        return _clean(uk.group("product"))
    ca = _CANADA_RECALL_TITLE.match(title)
    if ca:
        return _clean(ca.group("product"))
    match = _PRODUCT.search(title)
    if match is None:
        return None
    value = _PRODUCT_END.split(match.group("value"), maxsplit=1)[0]
    return _clean(value)


def _brand(text: str) -> str | None:
    match = _BRAND.search(text)
    if match is None:
        return None
    candidate = _BRAND_END.split(match.group("value"), maxsplit=1)[0]
    return _clean(candidate)


def _risk_type(text: str) -> str | None:
    types: set[str] = set()
    for category, expression in _RISK_PATTERNS.items():
        for match in expression.finditer(text):
            # Do not classify direct negations such as "inga spår av listeria".
            prefix = text[max(0, match.start() - 24):match.start()]
            if _NEGATION.search(prefix):
                continue
            types.add(category)
    # An explicitly undeclared allergen is more specific than generic mislabelling.
    if "allergen" in types:
        types.discard("labelling")
    if not types:
        return None
    return next(iter(types)) if len(types) == 1 else "multiple"


def _batches(text: str) -> tuple[str, ...]:
    found: list[str] = []
    for match in _BATCH_LABEL.finditer(text):
        section = _BATCH_STOP.split(match.group("values"), maxsplit=1)[0]
        # Process only clearly labelled, simple identifiers, not free-form numerics.
        for candidate in re.split(r"\s*(?:,|;|\boch\b|\band\b|/)\s*", section, flags=re.I):
            token = candidate.strip(" .:,;\t")
            if not _BATCH_TOKEN.fullmatch(token):
                continue
            if token.casefold() in {"och", "and", "samt", "nummer", "nr", "batch"}:
                continue
            if token not in found:
                found.append(token)
            if len(found) == MAX_ITEMS:
                return tuple(found)
    return tuple(found)


def _normalize_date(raw: str) -> str | None:
    try:
        words = raw.casefold().split()
        if len(words) == 3 and words[1] in _MONTHS:
            result = date(int(words[2]), _MONTHS[words[1]], int(words[0]))
        else:
            a, b, c = re.split(r"[-./]", raw)
            if len(a) == 4:
                result = date(int(a), int(b), int(c))
            else:
                result = date(int(c), int(b), int(a))
        return result.isoformat()
    except (ValueError, IndexError):
        return None


def _best_before(text: str) -> tuple[str, ...]:
    found: list[str] = []
    for match in _DATE_LABEL.finditer(text):
        # Only read a local window after an explicit best-before/use-by label.
        section = text[match.end():match.end() + 90]
        stop = re.search(r"[!?\n]|\b(?:batch|parti|risk\s+för|på\s+grund\s+av)\b", section, re.I)
        if stop is not None:
            section = section[:stop.start()]
        for date_match in _DATE_TOKEN.finditer(section):
            normalized = _normalize_date(date_match.group())
            if normalized and normalized not in found:
                found.append(normalized)
            if len(found) == MAX_ITEMS:
                return tuple(found)
    return tuple(found)


def extract_recall_details(title: str, summary: str) -> RecallDetails:
    """Read only supplied title/summary; do not scrape the linked article.

    Unknown product and brand are None; empty lists are not proof of absence.
    Results are candidate extractions to be checked against the original notice.
    """
    text = f"{title[:2048]} {summary[:2048]}"[:MAX_TEXT]
    return RecallDetails(
        product=_product(title[:2048]),
        brand=_brand(text),
        risk_type=_risk_type(text),
        batch_numbers=_batches(text),
        best_before_dates=_best_before(text),
    )
