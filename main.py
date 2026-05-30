import asyncio

from scraper import Scraper

if __name__ == '__main__':
    target_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC"

    scraper = Scraper(target_url)
    html = scraper.get_page_html()
    scraper.parse_offers(html)