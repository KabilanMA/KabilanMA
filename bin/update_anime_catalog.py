#!/usr/bin/env python3
"""Build _data/anime_catalog.json: every anime on MyAnimeList, most popular first.

Data comes from the public AniList API (https://anilist.co), which maps each show
to its MyAnimeList ID. Shows without a known start date are skipped.
Set "seen": true on a show to list it on the About page.
Re-running keeps every "seen" and "note" you have set.

Usage: python3 bin/update_anime_catalog.py
"""

import datetime
import json
import pathlib
import time
import urllib.error
import urllib.request

CATALOG = pathlib.Path(__file__).resolve().parent.parent / "_data" / "anime_catalog.json"
API = "https://graphql.anilist.co"
QUERY = """
query ($page: Int, $from: FuzzyDateInt, $to: FuzzyDateInt) {
  Page(page: $page, perPage: 50) {
    pageInfo { hasNextPage }
    media(type: ANIME, sort: POPULARITY_DESC, isAdult: false, startDate_greater: $from, startDate_lesser: $to) {
      idMal
      popularity
      title { romaji english }
      format
      episodes
      seasonYear
      startDate { year }
    }
  }
}
"""
# AniList stops paging a query after 5,000 results, so fetch one start year at a time.
FIRST_YEAR = 1900


def fetch_page(page, year):
    # Both bounds are exclusive; a year-only date is stored as YYYY0000.
    variables = {"page": page, "from": year * 10000 - 1, "to": (year + 1) * 10000}
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    request = urllib.request.Request(
        API,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            # AniList's firewall rejects Python's default User-Agent
            "User-Agent": "kabilan.info anime catalog (bin/update_anime_catalog.py)",
        },
    )
    for attempt in range(8):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)["data"]["Page"]
        except urllib.error.HTTPError as error:
            if error.code != 429 and error.code < 500:
                raise
            wait = int(error.headers.get("Retry-After") or 0) or 2**attempt
        except (urllib.error.URLError, TimeoutError):
            wait = 2**attempt
        print(f"  {year} page {page}: retrying in {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"{year} page {page} failed repeatedly")


def main():
    kept = {}
    if CATALOG.exists():
        for show in json.loads(CATALOG.read_text()):
            extra = {k: show[k] for k in ("seen", "note", "display_title") if show.get(k)}
            if extra:
                kept[show["mal_id"]] = extra

    found = {}
    for year in range(FIRST_YEAR, datetime.date.today().year + 3):
        page = 1
        while True:
            result = fetch_page(page, year)
            time.sleep(2.1)  # stay under AniList's rate limit
            for media in result["media"]:
                mal_id = media["idMal"]
                if not mal_id or mal_id in found:
                    continue
                found[mal_id] = (
                    media["popularity"] or 0,
                    {
                        "seen": False,
                        "mal_id": mal_id,
                        "title": media["title"]["romaji"],
                        "title_english": media["title"]["english"],
                        "type": media["format"],
                        "year": media["seasonYear"] or media["startDate"]["year"],
                        "episodes": media["episodes"],
                        "url": f"https://myanimelist.net/anime/{mal_id}",
                        **kept.get(mal_id, {}),
                    },
                )
            if not result["pageInfo"]["hasNextPage"]:
                break
            page += 1
        if year % 10 == 9:
            print(f"through {year}: {len(found)} shows")

    shows = [show for _, show in sorted(found.values(), key=lambda entry: -entry[0])]

    # One show per line so it's easy to search for a title and flip "seen".
    lines = ",\n".join(json.dumps(show, ensure_ascii=False) for show in shows)
    CATALOG.write_text(f"[\n{lines}\n]\n")
    print(f"wrote {len(shows)} shows to {CATALOG} ({sum(s['seen'] for s in shows)} seen)")


if __name__ == "__main__":
    main()
