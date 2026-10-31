"""Read-only live official-source probe; does not replace human or HA verification."""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sys

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "custom_components" / "recall_watch"))
from _client import RecallClient, SOURCES


async def check_source(session: aiohttp.ClientSession, source_id: str) -> dict:
    result = {"source": source_id, "checked_at": datetime.now(timezone.utc).isoformat(),
              "status": "failed", "record_count": 0}
    try:
        notices = await RecallClient(session, source_id).async_get_notices()
        if not notices:
            raise ValueError("No notices in live response")
        if any(notice.source_id != source_id for notice in notices):
            raise ValueError("Unexpected source identifier")
        if not any(notice.url and notice.url.startswith("https://") for notice in notices):
            raise ValueError("No verifiable authority link in response")
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {str(exc)[:180]}"
        if exc.__cause__ is not None:
            result["parse_cause"] = f"{type(exc.__cause__).__name__}: {str(exc.__cause__)[:180]}"
        # Diagnostic requests use only the same fixed government endpoints and
        # record metadata plus a bounded public-response prefix. No credentials.
        from _client.sources import SOURCES as SOURCE_REGISTRY
        source = SOURCE_REGISTRY[source_id]
        params = {"LastPublishDateStart": (datetime.now(timezone.utc) - timedelta(days=90)).date().isoformat()} if source.feed_format == "cpsc_json" else None
        try:
            async with session.get(source.url, params=params,
                                   headers={"Accept": "application/json" if source.feed_format == "cpsc_json" else "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9"},
                                   timeout=20, max_redirects=3) as response:
                preview = await response.content.read(2 * 1024 * 1024 + 1)
                result["diagnostic"] = {
                    "http_status": response.status,
                    "content_type": response.headers.get("Content-Type", "")[:100],
                    "response_bytes_prefix": preview.decode("utf-8", "replace")[:100],
                    "final_host": response.url.host,
                    "content_length_header": response.headers.get("Content-Length", ""),
                    "bytes_read_bounded": len(preview),
                    "exceeds_2mb_limit": len(preview) > 2 * 1024 * 1024,
                }
        except Exception as diagnostic_error:
            result["diagnostic_error"] = type(diagnostic_error).__name__
    else:
        result.update({
            "status": "parsed",
            "record_count": len(notices),
            "sample_notices_for_manual_review": [
                {
                    "identifier": item.identifier[:100],
                    "title": item.title[:160],
                    "url": item.url,
                    "published": item.published.isoformat() if item.published else None,
                    "updated": item.updated.isoformat() if item.updated else None,
                    "product": item.details.product,
                    "brand": item.details.brand,
                    "risk_type": item.details.risk_type,
                    "batch_numbers": list(item.details.batch_numbers[:3]),
                }
                for item in notices[:2]
            ],
        })
    return result


async def run(sources: list[str]) -> dict:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=75)) as session:
        records = []
        for source in sources:
            print(f"Probing {source}...", file=sys.stderr)
            records.append(await check_source(session, source))
    return {"checked_at": datetime.now(timezone.utc).isoformat(),
            "probe_only": True, "source_results": records,
            "all_parsed": all(item["status"] == "parsed" for item in records)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", choices=sorted(SOURCES))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = asyncio.run(run(args.source or list(SOURCES)))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["all_parsed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
