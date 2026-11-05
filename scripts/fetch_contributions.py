import os
import json
import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv("GITHUB_USERNAME", "ismailman81f")
URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
if response.status_code != 200:
    raise RuntimeError(f"Failed to fetch contributions: HTTP {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")
days = []
total_contributions = 0

for td in soup.find_all("td", class_="ContributionCalendar-day"):
    date = td.get("data-date")
    level = td.get("data-level", "0")
    count = 0
    tooltip_id = td.get("aria-describedby")
    if tooltip_id:
        tooltip = soup.find(id=tooltip_id)
        if tooltip:
            txt = tooltip.text.strip()
            parts = txt.split()
            if parts and parts[0].isdigit():
                count = int(parts[0])

    if date:
        days.append({
            "date": date,
            "level": int(level),
            "count": count
        })
        total_contributions += count

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump({"username": USERNAME, "total": total_contributions, "days": days}, f, indent=2)

print(f"Successfully saved {len(days)} days of contributions for {USERNAME}.")
