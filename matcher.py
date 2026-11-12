import difflib
import json
import math
from pathlib import Path

# Official commodity name -> spoken variations (English, Hindi, Marathi)
COMMODITIES = {
    "Onion": ["onion", "pyaaz", "pyaz", "pyaj", "kanda", "प्याज", "कांदा"],
    "Tomato": ["tomato", "tamatar", "tamater", "टमाटर", "टोमॅटो"],
    "Potato": ["potato", "aloo", "batata", "आलू", "बटाटा"],
    "Brinjal": ["brinjal", "baingan", "vangi", "बैंगन", "वांगी"],
    "Cabbage": ["cabbage", "patta gobhi", "kobi", "पत्ता गोभी", "कोबी"],
}

MANDIS = {
    m["name"]: m
    for m in json.loads((Path(__file__).parent / "mandis.json").read_text(encoding="utf-8"))
}
MANDI_ALIASES = {name: m["aliases"] for name, m in MANDIS.items()}


def _find(text, table):
    lowered = text.lower()
    # 1. Exact substring match
    for key, aliases in table.items():
        if any(alias in lowered for alias in aliases):
            return key
    # 2. Fuzzy match on each word as a fallback
    all_aliases = {alias: key for key, aliases in table.items() for alias in aliases}
    for word in lowered.split():
        word = word.strip(".,?!।")
        match = difflib.get_close_matches(word, all_aliases, n=1, cutoff=0.8)
        if match:
            return all_aliases[match[0]]
    return None


def find_commodity(text):
    return _find(text, COMMODITIES)


def find_mandi(text):
    return _find(text, MANDI_ALIASES)


def km_between(a, b):
    """Straight-line distance in km between two mandis (haversine formula)."""
    r = 6371
    lat1, lat2 = math.radians(a["lat"]), math.radians(b["lat"])
    dlat = lat2 - lat1
    dlon = math.radians(b["lon"] - a["lon"])
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))