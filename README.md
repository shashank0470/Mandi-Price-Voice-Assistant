# Mandi Price Voice Assistant

## The problem
Farmers often sell at the nearest mandi without knowing that a mandi 40 km away is paying more today. The prices are public on Agmarknet (data.gov.in) but hard to use on a basic phone.

## What it does
A farmer asks, by voice or text, in English, Hindi or Marathi: "aaj Nashik mandi mein pyaaz ka bhav kya hai". The app returns today's min, max and modal price for that crop, plus the best-paying mandi within the chosen distance. It reads the answer aloud. If today's data is missing, it says so.

## Data
- Source: Agmarknet daily mandi prices via data.gov.in (resource `9ef84268-d588-465a-a308-a864a43d0070`)
- Prices are per quintal. Only real data from the API is shown. Nothing is made up.

## How to run
1. Get a free API key from data.gov.in.
2. Copy `.env.example` to `.env` and paste your key:
   `DATA_GOV_API_KEY=your_key_here`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the app:
   `python app.py`
5. Open http://127.0.0.1:5000 in Chrome.
6. Pick a language and your town, then type a question or tap "Speak question".

Example questions:
- "aaj Nashik mandi mein pyaaz ka bhav kya hai"
- "tomato price in Pune"
- "नाशिक मंडी में कांदा का भाव"

## Architecture
- `static/index.html`: the UI. Browser speech recognition handles voice input, and browser speech synthesis reads the reply aloud.
- `app.py`: Flask server with `/api/ask`. It finds the crop and mandi, fetches prices, filters by distance, and builds the reply.
- `agmarknet.py`: calls the data.gov.in API.
- `matcher.py`: matches spoken names to official crop and mandi names using a lookup table, with fuzzy matching as a fallback. It also computes distance between towns.
- `mandis.json`: mandi names, approximate coordinates, and spoken aliases.

## Not included (on purpose)
Price prediction.

## Cost per run
₹0. Agmarknet data, the browser's speech features, and a local Flask server are all free.

## What broke and how I fixed it
(Fill this in after testing.)