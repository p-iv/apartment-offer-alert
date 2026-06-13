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
    def parse_row_html(html_content: str) -> dict:
        if not html_content:
            print("[ERROR] no data for parsing")
            return {}

        soup = BeautifulSoup(html_content, "html.parser")
        script_tag = soup.find("script", {"type": "application/ld+json"})

        if not script_tag:
            print("[ERROR] no json found for parsing")
            return {}

        try:
            data_json = json.loads(script_tag.string)
            graph = data_json.get("@graph", [])
            row_json_dict = {}

            for item in graph:
                if "offers" in item and "offers" in item["offers"]:
                    row_json_dict = item["offers"]["offers"]
                    break

            if not row_json_dict:
                print("[WARNING] Structure found, but offers array is empty.")

            return row_json_dict

        except (IndexError, KeyError, json.JSONDecodeError) as e:
            print(f"[ERROR] while parsing json : {e}")
            return {}

    @staticmethod
    def parse_offers(row_json: dict) -> list:
        if not row_json:
            print("[ERROR] no data for parsing")
            return []

        parsed_json_list = []

        for item in row_json:
            name = item.get("name")
            price = item.get("price", 0)
            image = item.get("image", "")
            url = item.get("url", "")

            item_details = item.get("itemOffered", {})
            description = item_details.get("description", "")
            num_rooms = item_details.get("numberOfRooms", 0)

            apartment_size = item_details.get("floorSize", {}).get("value", 0)
            price_per_m2 = round(price / apartment_size, 2) if apartment_size > 0 else 0

            address_details = item_details.get("address", {})
            city = address_details.get("addressLocality", "")
            street = address_details.get("streetAddress", "")

            parsed_json = {
                "title": name,
                "image": image,
                "price": price,
                "url": url,
                "description": description,
                "num_rooms": num_rooms,
                "apartment_size": apartment_size,
                "price_per_m2": price_per_m2,
                "city": city,
                "street": street,
            }

            parsed_json_list.append(parsed_json)

        return parsed_json_list
