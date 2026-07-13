import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://www.bankofamerica.com"
START_URL = "https://www.bankofamerica.com/credit-cards/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# -------------------------
# Step 1 : Get Landing Page
# -------------------------

landing_soup = get_soup(START_URL)

# -------------------------
# Step 2 : Find Product Links
# -------------------------

card_links = set()

for link in landing_soup.find_all("a", href=True):

    href = link["href"]

    if "/credit-cards/" in href and "apply" not in href:

        full_url = urljoin(BASE_URL, href)

        card_links.add(full_url)

print(f"Found {len(card_links)} pages")

# -------------------------
# Step 3 : Visit each page
# -------------------------

cards = []

for url in sorted(card_links):

    try:

        print("Scraping:", url)

        soup = get_soup(url)

        # --------------------
        # Card Name
        # --------------------

        h1 = soup.find("h1")

        card_name = h1.get_text(strip=True) if h1 else "Unknown"

        # --------------------
        # Category
        # --------------------

        category = ""

        breadcrumbs = soup.find_all("li")

        if breadcrumbs:
            category = breadcrumbs[-2].get_text(strip=True) if len(breadcrumbs) > 1 else ""

        # --------------------
        # Features
        # --------------------

        features = []

        for li in soup.find_all("li"):

            text = li.get_text(" ", strip=True)

            if len(text) > 30:
                features.append(text)

        # remove duplicates

        features = list(dict.fromkeys(features))

        # --------------------
        # Description
        # --------------------

        description = ""

        p = soup.find("p")

        if p:
            description = p.get_text(" ", strip=True)

        # --------------------
        # Benefits
        # --------------------

        benefits = " ".join(features[:5])

        # --------------------
        # Rates & Fees
        # --------------------

        rates = []

        page_text = soup.get_text(" ", strip=True)

        keywords = [
            "APR",
            "annual fee",
            "balance transfer",
            "interest rate",
            "foreign transaction fee"
        ]

        sentences = page_text.split(".")

        for sentence in sentences:

            for key in keywords:

                if key.lower() in sentence.lower():

                    rates.append(sentence.strip())

                    break

        rates = list(dict.fromkeys(rates))

        cards.append(
            {
                "card_name": card_name,
                "category": category,
                "description": description,
                "features": features,
                "benefits": benefits,
                "rates_fees": rates,
                "source": url,
            }
        )

    except Exception as e:

        print("Skipped:", url)
        print(e)

# -------------------------
# Save JSON
# -------------------------

with open("data/raw_data.json", "w", encoding="utf-8") as f:

    json.dump(cards, f, indent=4, ensure_ascii=False)

print("Done")

