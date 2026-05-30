import json

from curl_cffi import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_page_html(self) -> str:
        response = requests.get(self.base_url, impersonate="chrome")

        if response.status_code == 200:
            print("[SUCCESS] data has been fetched")
            return response.text
        else:
            print("[ERROR] data failed to fetch")
            return ""

    @staticmethod
    def parse_offers(html_content: str):
        if not html_content:
            print("[ERROR] no data for parsing")
            return

        soup = BeautifulSoup(html_content, "html.parser")
        script_tag = soup.find("script", {"type": "application/ld+json"})

        if not script_tag:
            print("[ERROR] no json found for parsing")
            return

        try:
            data_json = json.loads(script_tag.string)
            offers_list = data_json["@graph"][1]["offers"]["offers"]

            for i, offer in enumerate(offers_list, start=1):
                title = offer.get("name")
                price = offer.get("price", 0)
                url = offer.get("url", "")

                item_details = offer.get("itemOffered", {})
                description = item_details.get("description", "")
                num_rooms = item_details.get("numberOfRooms", 0)

                apartment_size = item_details.get("floorSize", {}).get("value", 0)
                price_per_m2 = round(price / apartment_size, 2) if apartment_size > 0 else 0

                print(f"Offer #{i}: {title}")
                print(f"Description: {description}")
                print(f"       Price: {price} PLN | Meters: {apartment_size} m² | Rooms: {num_rooms}")
                print(f"       Price per m²: {price_per_m2} PLN")
                print(f"       Url: {url}")
                print("-" * 70)

        except (IndexError, KeyError, json.JSONDecodeError) as e:

            print(f"[Scraper] Błąd podczas przetwarzania struktury JSON: {e}")

