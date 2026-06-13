# Apartment Offer Alert 

An automated, real-time web scraping and data analysis system designed to monitor the real estate market (Otodom) for rental apartments. The application automatically detects new listings, calculates market price averages using an internal database, filters out price anomalies, and instantly sends automated alerts via a Telegram bot.

---

## Features

* **Real-time Web Scraping:** Automated extraction of rental data including price, size, price per m², and cover images.
* **Smart Duplication Filter:** Relies on an SQLite backend to ensure that previously processed URLs are never processed or sent twice.
* **Algorithmic Deal Detection:** Automatically calculates global and historical moving price averages to flag properties listed at 15% (or more) below the current market rate.
* **Instant Telegram Alerts:** Leverages `python-telegram-bot` to push formatted HTML rich notifications (with images and clickable direct links) straight to your phone.

---

## Tech Stack

* **Backend & Logic:** Python 3.x
* **Data Storage:** SQLite 3 
* **Messaging API:** `python-telegram-bot`
* **Scraping Infrastructure:** curl_cffi and bs4

---

## Project Architecture & Workflow

1. **Scraper Engine:** Boots up every 15 minutes.
2. **Database Verification:** Checks if the scraped URL exists in the main pipeline.
3. **Data Analysis:** If the entry is new, the system triggers `SELECT AVG(price_per_m2) FROM apartments` to fetch the real-time average.
4. **Conditional Routing:** * The entry is saved into the master `apartments` table.
   * If `current_price_per_m2 < market_avg * 0.85`, it is copied into the `valuable_offers` table and triggers an immediate high-priority Telegram push.
5. **Sleep Sequence:** The process safely closes database connections and enters sleep cycle.

---
(https://github.com/YOUR_GITHUB_USERNAME/apartment-offer-alert.git)
cd apartment-offer-alert
