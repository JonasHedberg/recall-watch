"""Read-only live official-source probe; does not replace human or HA verification."""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
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
    else:
        result.update({"status": "parsed", "record_count": len(notices)})
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
