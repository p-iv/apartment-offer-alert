import time
from scraper import Scraper
from database import SQLliteDB
from telegram_bot import send_telegram_notification

def start_program():
    fetch_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC"

    scraper = Scraper(fetch_url)
    try:
        row_html = scraper.get_page_html()
        row_json = scraper.parse_row_html(row_html)
        parsed_offers = scraper.parse_offers(row_json)
    except Exception as e:
        print("[ERROR] something went wrong" + str(e))
        return


    db = SQLliteDB("../database/otodom.db")

    new_offers = 0
    valuable_offers = 0

    for offer in parsed_offers:
        if db.is_new_offer(offer['url']):
            if db.is_valuable_offer(offer['price_per_m2']):
                db.insert_new_offer(offer, "valuable_offers")
                valuable_offers += 1
                send_telegram_notification(offer, is_valuable=True)
            new_offers += 1
            db.insert_new_offer(offer, "apartments")
            send_telegram_notification(offer, is_valuable=False)

    db.close_connection()
    print(f"Process finished with {new_offers} new offers and {valuable_offers} valuable offers")

if __name__ == '__main__':
    print("=== MONITORING OF VALUABLE OFFERS IS ON ===")
    while True:
        try:
            start_program()
        except Exception as main_error:
            print("[ERROR] " + str(main_error))

        time.sleep(900)

    # target_excel_path = "../generated_excel/otodom.xlsx"
    # analyzer = Analyzer(parsed_offers, target_excel_path)
    #
    # analyzer.clean_data()
    # analyzer.generate_excel()


