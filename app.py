import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from agmarknet import fetch_prices
from matcher import MANDIS, MANDI_ALIASES, find_commodity, find_mandi, km_between

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="")
API_KEY = os.getenv("DATA_GOV_API_KEY", "")
STATE = "Maharashtra"

REPLIES = {
    "en": {
        "no_crop": "I did not catch the crop name. Please say it again.",
        "no_key": "The data.gov.in API key is not set. Add it to the .env file.",
        "no_data": "Sorry, today's price data is not available for {crop}.",
        "no_mandi": "Sorry, today's {crop} price is not available for {mandi}.",
        "price": (
            "{market} mandi {crop} price: Rs {modal} per quintal "
            "(min {min}, max {max}), data date {date}. "
            "Best nearby: {best} at Rs {best_modal}, {km} km from {base}."
        ),
    },
    "hi": {
        "no_crop": "फसल का नाम समझ नहीं आया। कृपया दोबारा बोलिए।",
        "no_key": "data.gov.in की API key सेट नहीं है। .env फ़ाइल में जोड़ें।",
        "no_data": "माफ़ कीजिए, {crop} का आज का भाव उपलब्ध नहीं है।",
        "no_mandi": "माफ़ कीजिए, {mandi} में {crop} का आज का भाव उपलब्ध नहीं है।",
        "price": (
            "{market} मंडी में {crop} का भाव: Rs {modal} प्रति क्विंटल "
            "(न्यूनतम {min}, अधिकतम {max}), डेटा तारीख {date}। "
            "आसपास सबसे अच्छा भाव: {best} में Rs {best_modal}, {base} से {km} किमी।"
        ),
    },
    "mr": {
        "no_crop": "पिकाचे नाव समजले नाही. कृपया पुन्हा सांगा.",
        "no_key": "data.gov.in ची API key सेट केलेली नाही. .env फाईलमध्ये जोडा.",
        "no_data": "क्षमस्व, {crop} चा आजचा भाव उपलब्ध नाही.",
        "no_mandi": "क्षमस्व, {mandi} येथे {crop} चा आजचा भाव उपलब्ध नाही.",
        "price": (
            "{market} बाजारात {crop} चा भाव: Rs {modal} प्रति क्विंटल "
            "(किमान {min}, कमाल {max}), डेटा तारीख {date}. "
            "जवळचा सर्वोत्तम भाव: {best} येथे Rs {best_modal}, {base} पासून {km} किमी."
        ),
    },
}


def _date(record):
    try:
        return datetime.strptime(record.get("arrival_date", ""), "%d/%m/%Y")
    except ValueError:
        return datetime.min


def _price(record):
    try:
        return float(record.get("modal_price") or 0)
    except ValueError:
        return 0.0


def mandi_from_market(market):
    """Map a dataset market name such as 'APMC Kolhapur' to a mandi in mandis.json."""
    text = (market or "").lower()
    for name, aliases in MANDI_ALIASES.items():
        if any(alias in text for alias in aliases):
            return name
    return None


def latest_per_market(records):
    """Keep the newest record for each known mandi."""
    latest = {}
    for record in records:
        name = mandi_from_market(record.get("market"))
        if not name:
            continue
        if name not in latest or _date(record) > _date(latest[name]):
            latest[name] = record
    return latest


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/mandis")
def mandis():
    return jsonify(sorted(MANDIS))


@app.route("/api/ask", methods=["POST"])
def ask():
    body = request.get_json(force=True)
    text = body.get("text", "")
    lang = body.get("lang", "en")
    if lang not in REPLIES:
        lang = "en"
    msg = REPLIES[lang]
    base = body.get("base", "Nashik")
    if base not in MANDIS:
        base = "Nashik"
    max_km = float(body.get("max_km") or 50)

    crop = find_commodity(text)
    if not crop:
        return jsonify(reply=msg["no_crop"])
    if not API_KEY:
        return jsonify(reply=msg["no_key"])

    try:
        records = fetch_prices(crop, STATE, API_KEY)
    except Exception as e:
        print("API error:", e)
        return jsonify(reply=msg["no_data"].format(crop=crop))

    latest = latest_per_market(records)
    print("Records from API:", len(records))
    print("Matched markets:", list(latest.keys()))
    named = find_mandi(text)
    base_mandi = MANDIS[base]

    nearby = []
    for name, record in latest.items():
        km = km_between(base_mandi, MANDIS[name])
        if km <= max_km or name == named:
            nearby.append((name, km, record))

    if not nearby:
        return jsonify(reply=msg["no_data"].format(crop=crop))

    best_name, best_km, best_record = max(nearby, key=lambda item: _price(item[2]))

    if named:
        if named not in latest:
            return jsonify(reply=msg["no_mandi"].format(crop=crop, mandi=named))
        target_name, target_record = named, latest[named]
    else:
        target_name, target_record = best_name, best_record

    reply = msg["price"].format(
        market=target_name,
        crop=crop,
        modal=target_record.get("modal_price"),
        min=target_record.get("min_price"),
        max=target_record.get("max_price"),
        date=target_record.get("arrival_date"),
        best=best_name,
        best_modal=best_record.get("modal_price"),
        km=round(best_km),
        base=base,
    )
    return jsonify(reply=reply, crop=crop, market=target_name)


if __name__ == "__main__":
    app.run(debug=True)