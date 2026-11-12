import json
import time
from pathlib import Path

import requests

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_SECONDS = 6 * 60 * 60

# Set to True for the video (uses the saved real records below).
# Set to False to call the live API again.
USE_SAVED_DATA = True



# Real records copied from data.gov.in. A crop with [] has no saved data yet.
SAVED_RECORDS = {
    "Onion": [
        {"state": "Maharashtra", "district": "Chattrapati Sambhajinagar", "market": "APMC Chattrapati Sambhajinagar ", "commodity": "Onion", "variety": "Other", "grade": "Local", "arrival_date": "11/11/2026", "min_price": 2200, "max_price": 4600, "modal_price": 3400},
        {"state": "Maharashtra", "district": "Kolhapur", "market": "APMC Kolhapur", "commodity": "Onion", "variety": "Other", "grade": "Local", "arrival_date": "11/11/2026", "min_price": 1000, "max_price": 5100, "modal_price": 3200},
        {"state": "Maharashtra", "district": "Pune", "market": "Khed(Chakan) ", "commodity": "Onion", "variety": "Other", "grade": "Local", "arrival_date": "11/11/2026", "min_price": 2500, "max_price": 4600, "modal_price": 3500},
        {"state": "Maharashtra", "district": "Ahilyanagar", "market": "APMC Karjat ", "commodity": "Onion", "variety": "Local", "grade": "Local", "arrival_date": "11/11/2026", "min_price": 500, "max_price": 4000, "modal_price": 2000},
        {"state": "Maharashtra", "district": "Pune", "market": "Pune(Pimpri) ", "commodity": "Onion", "variety": "Local", "grade": "Local", "arrival_date": "11/11/2026", "min_price": 3300, "max_price": 4700, "modal_price": 4000},
    ],
    "Tomato": [
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "APMC Pune ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1600,
            "modal_price": 1100
        },
        {
            "state": "Maharashtra",
            "district": "Satara",
            "market": "APMC Patan",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1250,
            "max_price": 1450,
            "modal_price": 1350
        },
        {
            "state": "Maharashtra",
            "district": "Satara",
            "market": "APMC Satara ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1500,
            "modal_price": 1250
        },
        {
            "state": "Maharashtra",
            "district": "Solapur",
            "market": "APMC Akluj ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1600,
            "modal_price": 1300
        },
        {
            "state": "Maharashtra",
            "district": "Mumbai",
            "market": "APMC Mumbai ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1400,
            "modal_price": 1200
        },
        {
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "market": "APMC Ratnagiri (Nachane) ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 1000,
            "modal_price": 800
        },
        {
            "state": "Maharashtra",
            "district": "Solapur",
            "market": "APMC Solapur ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 300,
            "max_price": 2200,
            "modal_price": 1200
        },
        {
            "state": "Maharashtra",
            "district": "Solapur",
            "market": "APMC Mangal Wedha ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 2200,
            "modal_price": 1800
        },
        {
            "state": "Maharashtra",
            "district": "Jalgaon",
            "market": "APMC Bhusaval ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 1000,
            "modal_price": 800
        },
        {
            "state": "Maharashtra",
            "district": "Nagpur",
            "market": "APMC Nagpur ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1700,
            "max_price": 2200,
            "modal_price": 2075
        },
        {
            "state": "Maharashtra",
            "district": "Kolhapur",
            "market": "APMC Kolhapur",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 1000,
            "modal_price": 800
        },
        {
            "state": "Maharashtra",
            "district": "Ahilyanagar",
            "market": "APMC Shrirampur ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1400,
            "modal_price": 1200
        },
        {
            "state": "Maharashtra",
            "district": "Chandrapur",
            "market": "Chandrapur(Ganjwad) ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1600,
            "modal_price": 1200
        },
        {
            "state": "Maharashtra",
            "district": "Chattrapati Sambhajinagar",
            "market": "APMC Chattrapati Sambhajinagar ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1200,
            "modal_price": 900
        },
        {
            "state": "Maharashtra",
            "district": "Nagpur",
            "market": "APMC Kamthi ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 2000,
            "max_price": 2500,
            "modal_price": 2350
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Khed(Chakan) ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1800,
            "modal_price": 1400
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Pune(Moshi) ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1000,
            "modal_price": 900
        },
        {
            "state": "Maharashtra",
            "district": "Sangli",
            "market": "APMC Vita ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1200,
            "modal_price": 1000
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Pune(Pimpri) ",
            "commodity": "Tomato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1300,
            "max_price": 1500,
            "modal_price": 1400
        },
        {
            "state": "Maharashtra",
            "district": "Ahilyanagar",
            "market": "APMC Rahuri ",
            "commodity": "Tomato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 2000,
            "modal_price": 1500
        }
    ],
    "Potato": [
                {
            "state": "Maharashtra",
            "district": "Akola",
            "market": "APMC Akola ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1200,
            "modal_price": 900
        },
        {
            "state": "Maharashtra",
            "district": "Chattrapati Sambhajinagar",
            "market": "APMC Chattrapati Sambhajinagar ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1200,
            "modal_price": 900
        },
        {
            "state": "Maharashtra",
            "district": "Solapur",
            "market": "APMC Akluj ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1500,
            "max_price": 1800,
            "modal_price": 1600
        },
        {
            "state": "Maharashtra",
            "district": "Ahilyanagar",
            "market": "APMC Shrirampur ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1500,
            "modal_price": 1250
        },
        {
            "state": "Maharashtra",
            "district": "Nagpur",
            "market": "APMC Kamthi ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 2000,
            "max_price": 2500,
            "modal_price": 2350
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Khed(Chakan) ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1100,
            "max_price": 1700,
            "modal_price": 1300
        },
        {
            "state": "Maharashtra",
            "district": "Sangli",
            "market": "Sangli(Phale, Bhajipala Market) ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1600,
            "modal_price": 1300
        },
        {
            "state": "Maharashtra",
            "district": "Satara",
            "market": "APMC Vaduj ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1400,
            "max_price": 1600,
            "modal_price": 1500
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "APMC Pune ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 2200,
            "modal_price": 1600
        },
        {
            "state": "Maharashtra",
            "district": "Satara",
            "market": "APMC Satara ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1200,
            "max_price": 1600,
            "modal_price": 1400
        },
        {
            "state": "Maharashtra",
            "district": "Mumbai",
            "market": "Mumbai-Onion & Potato Market ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1300,
            "modal_price": 950
        },
        {
            "state": "Maharashtra",
            "district": "Nagpur",
            "market": "APMC Nagpur ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1100,
            "modal_price": 1025
        },
        {
            "state": "Maharashtra",
            "district": "Jalgaon",
            "market": "APMC Bhusaval ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1200,
            "max_price": 2000,
            "modal_price": 1500
        },
        {
            "state": "Maharashtra",
            "district": "Solapur",
            "market": "APMC Solapur ",
            "commodity": "Potato",
            "variety": "Local",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 900,
            "max_price": 1300,
            "modal_price": 1100
        },
        {
            "state": "Maharashtra",
            "district": "Ahilyanagar",
            "market": "APMC Rahata ",
            "commodity": "Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1200,
            "modal_price": 1100
        },
        {
            "state": "Maharashtra",
            "district": "Mumbai",
            "market": "APMC Mumbai ",
            "commodity": "Sweet Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1600,
            "max_price": 3000,
            "modal_price": 2300
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "APMC Pune ",
            "commodity": "Sweet Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 2000,
            "max_price": 3000,
            "modal_price": 2500
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Pune(Moshi) ",
            "commodity": "Sweet Potato",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 3000,
            "max_price": 3000,
            "modal_price": 3000
        }
    ],
    "Cabbage": [
        {
            "state": "Maharashtra",
            "district": "Ahilyanagar",
            "market": "APMC Shrirampur ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 700,
            "modal_price": 600
        },
        {
            "state": "Maharashtra",
            "district": "Jalgaon",
            "market": "APMC Bhusaval ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 800,
            "max_price": 1200,
            "modal_price": 1000
        },
        {
            "state": "Maharashtra",
            "district": "Kolhapur",
            "market": "APMC Kolhapur",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 1000,
            "modal_price": 800
        },
        {
            "state": "Maharashtra",
            "district": "Chattrapati Sambhajinagar",
            "market": "APMC Chattrapati Sambhajinagar ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 500,
            "max_price": 700,
            "modal_price": 600
        },
        {
            "state": "Maharashtra",
            "district": "Nagpur",
            "market": "APMC Nagpur ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 300,
            "max_price": 500,
            "modal_price": 450
        },
        {
            "state": "Maharashtra",
            "district": "Satara",
            "market": "APMC Satara ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 600,
            "max_price": 800,
            "modal_price": 700
        },
        {
            "state": "Maharashtra",
            "district": "Pune",
            "market": "Pune(Pimpri) ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 1000,
            "max_price": 1000,
            "modal_price": 1000
        },
        {
            "state": "Maharashtra",
            "district": "Chandrapur",
            "market": "Chandrapur(Ganjwad) ",
            "commodity": "Cabbage",
            "variety": "Other",
            "grade": "Local",
            "arrival_date": "12/11/2026",
            "min_price": 400,
            "max_price": 600,
            "modal_price": 500
        }
    ],
}


def _cache_file(commodity, state):
    safe = f"{state}_{commodity}".replace(" ", "_")
    return CACHE_DIR / f"{safe}.json"


def fetch_prices(commodity, state, api_key, limit=100):
    """Return mandi price records for one commodity in one state."""
    if USE_SAVED_DATA:
        records = [
        r for r in SAVED_RECORDS.get(commodity, [])
        if r.get("commodity", "").strip().lower() == commodity.lower()
    ]
    print(f"Saved data for {commodity}: {len(records)} records")
    return records

    CACHE_DIR.mkdir(exist_ok=True)
    cache = _cache_file(commodity, state)

    if cache.exists() and time.time() - cache.stat().st_mtime < CACHE_SECONDS:
        return json.loads(cache.read_text(encoding="utf-8-sig"))

    params = {
        "api-key": api_key,
        "format": "json",
        "limit": limit,
        "filters[state]": state,
        "filters[commodity]": commodity,
    }
    try:
        response = requests.get(URL, params=params, timeout=60)
        response.raise_for_status()
        records = response.json().get("records", [])
    except Exception:
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8-sig"))
        raise

    if records:
        cache.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return records