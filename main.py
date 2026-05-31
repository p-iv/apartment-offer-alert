import analyzer
from analyzer import Analyzer
from scraper import Scraper

if __name__ == '__main__':
    fetch_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC"
    target_excel_path = "generated_excel/atodom.xlsx"

    scraper = Scraper(fetch_url)
    analyzer = Analyzer(scraper.parsed_json, target_excel_path)