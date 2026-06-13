
from analyzer import Analyzer
from scraper import Scraper
from src.database import SQLliteDB

if __name__ == '__main__':
    fetch_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC"
    target_excel_path = "../generated_excel/otodom.xlsx"

    scraper = Scraper(fetch_url)

    row_html = scraper.get_page_html()
    row_json = scraper.parse_row_html(row_html)
    parsed_offers = scraper.parse_offers(row_json)

    analyzer = Analyzer(parsed_offers, target_excel_path)

    analyzer.clean_data()
    analyzer.generate_excel()

    db = SQLliteDB("../database/otodom.db")

    for offer in parsed_offers:
        if db.is_new_offer(offer['url']):
            if db.is_valuable_offer(offer['price_per_m2']):
                db.insert_new_offer(offer, "valuable_offers")
            db.insert_new_offer(offer, "apartments")


