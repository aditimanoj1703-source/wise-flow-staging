"""
Downloads player images from Wikimedia Commons using the public API.
Images are saved to players/images/ and named by player slug.
"""

import json
import os
import time
import urllib.request
import urllib.parse

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
METADATA_FILE = os.path.join(os.path.dirname(__file__), "metadata.json")
API_BASE = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "WiseFlowStagingBot/1.0 (YouTube Shorts content; educational use)"


def get_image_url(wikimedia_filename):
    """Query Wikimedia Commons API for the direct image URL."""
    decoded_name = urllib.parse.unquote(wikimedia_filename)
    title = f"File:{decoded_name}"
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    })
    req = urllib.request.Request(
        f"{API_BASE}?{params}",
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    imageinfo = page.get("imageinfo")
    if not imageinfo:
        return None
    return imageinfo[0]["url"]


def download_image(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(dest_path, "wb") as f:
            f.write(resp.read())


def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    with open(METADATA_FILE) as f:
        players = json.load(f)

    results = []
    for player in players:
        dest = os.path.join(IMAGES_DIR, player["image_file"])
        if os.path.exists(dest):
            print(f"  [skip] {player['name']} — already downloaded")
            results.append({**player, "status": "cached"})
            continue

        print(f"  [fetch] {player['name']} ({player['wikimedia_file']}) …", end=" ", flush=True)
        try:
            url = get_image_url(player["wikimedia_file"])
            if not url:
                raise ValueError("No imageinfo returned")
            download_image(url, dest)
            size_kb = os.path.getsize(dest) // 1024
            print(f"OK ({size_kb} KB)")
            results.append({**player, "status": "ok", "source_url": url})
        except Exception as e:
            print(f"FAILED — {e}")
            results.append({**player, "status": "failed", "error": str(e)})

        time.sleep(0.5)  # be polite to Wikimedia

    ok = sum(1 for r in results if r["status"] in ("ok", "cached"))
    failed = [r for r in results if r["status"] == "failed"]
    print(f"\n{ok}/{len(players)} images ready.")
    if failed:
        print("Failed:", [r["name"] for r in failed])

    # Write download report
    report_path = os.path.join(os.path.dirname(__file__), "download_report.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
