# Mandi Vani: Mandi Price Voice Assistant

Voice assistant that tells farmers today's mandi prices for onion, tomato, potato and cabbage in English, Hindi and Marathi, and names the best-paying nearby mandi.

## The problem
Farmers often sell at the nearest mandi without knowing that a mandi 40 km away is paying more today. The prices are public on Agmarknet (data.gov.in), but hard to use on a basic phone.

## What it does
A farmer asks a question by voice or text, for example "pyaaz ka bhav Pune mein kya hai". The app:
1. Finds the crop and the mandi in the question.
2. Gets the price records for that crop in Maharashtra.
3. Keeps the latest price for each mandi.
4. Filters mandis within the chosen distance and picks the highest modal price.
5. Replies with the modal, minimum and maximum price per quintal, the data date, and the best nearby mandi.

If there is no data for the crop or mandi, the app says so instead of guessing.

## Data
- Source: Agmarknet daily mandi prices, data.gov.in, resource `9ef84268-d588-465a-a308-a864a43d0070`.
- The app uses a saved snapshot of real records copied from that source (Onion dated 11/11/2026, Tomato, Potato and Cabbage dated 12/11/2026). Prices are per quintal.
- Nothing is invented. Every price comes from the Agmarknet response.
- Sweet Potato records are excluded from Potato answers.
- A switch in `agmarknet.py` (`USE_SAVED_DATA`) turns on live calls to the API. Live calls use a local cache for 6 hours, and the app falls back to the cache if the API fails.

## How to run
1. Create and activate a virtual environment, then install the packages:
   `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your key:
   `DATA_GOV_API_KEY=your_key_here`
3. Start the app:
   `python app.py`
4. Open http://127.0.0.1:5000 in Chrome.
5. Set My town to Pune and Max distance to 300 km, then ask:
   - `pyaaz ka bhav Pune mein kya hai` (Onion)
   - `tamatar ka bhav Pune mein kya hai` (Tomato)
   - `aloo ka bhav Pune mein kya hai` (Potato)

## Architecture
- `static/index.html`: the UI. The browser's speech recognition turns voice into text, and the browser's speech synthesis reads the reply aloud.
- `app.py`: Flask server with `/api/ask`. It matches the crop and mandi, gets the records, filters by distance, picks the best mandi, and builds the reply.
- `agmarknet.py`: holds the saved records and the optional live API call with caching.
- `matcher.py`: matches spoken crop and mandi names in English, Hindi and Marathi, with fuzzy matching for typos. It also computes the distance between towns.
- `mandis.json`: mandi names, approximate coordinates and spoken aliases.

No LLM is used. Speech is handled by the browser, matching is keyword and fuzzy search, and the prices come from the Agmarknet records.

## Not included (on purpose)
Price prediction.

## Cost per run
₹0. Agmarknet data, the browser's speech features and the local Flask server are free.

## What broke and how I fixed it
- **The live API was failing during testing.** The data.gov.in endpoint returned timeouts and 502 errors while I was recording. The app therefore uses the saved Agmarknet records, and the live call can be turned back on with `USE_SAVED_DATA = False`.
- **Market names did not match.** The dataset uses names like "APMC Kolhapur", while my list had "Kolhapur", so every record was skipped. I now match by substring, so these names are recognised.
- **Date and crop-name issues in the saved records.** Some dates had stray backslashes, and "Sweet Potato" was matching "Potato". I cleaned the dates and filter records by exact crop name.