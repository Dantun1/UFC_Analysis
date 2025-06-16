from typing import Optional

import scrapy
import string
from ..items import FighterItem

class FightersSpider(scrapy.Spider):
    name = "fighters"
    allowed_domains = ["ufcstats.com"]

    def start_requests(self):
        self.logger.info("Starting Fighters Spider")
        base_url = "http://ufcstats.com/statistics/fighters"
        for letter in string.ascii_lowercase:
            yield scrapy.Request(f"{base_url}?char={letter}&page=all", callback=self.parse)



    def parse(self, response):
        fighter_links = set(response.css(".b-statistics__table-col > a::attr(href)").getall())
        if fighter_links:
            self.logger.info(f"Found {len(fighter_links)} unique fighter links")
        else:
            self.logger.warning("No fighter links found")

        for link in fighter_links:
            yield response.follow(link, callback=self.parse_fighter)

    def parse_fighter(self, response):
        item = FighterItem()

        # Manually add attributes with non-standard structures
        # Store name for reference in debugging
        name = response.css(".b-content__title-highlight::text").get().strip()
        item["name"] = name
        item["nickname"] = response.css(".b-content__Nickname::text").get().strip()
        item["record"] = response.css(".b-content__title-record::text").get().strip().split(":")[1].strip()


        def get_stat(stat_label: str) -> Optional[str]:
            xpath_selector = f"string(//li[contains(i/text(), '{stat_label}')])"

            # Stats are grabbed in the format "Label: Stat"
            raw_text = response.xpath(xpath_selector).get()

            # Return stripped second part of string (following the colon) if exists. Otherwise, return None.
            if not raw_text or ":" not in raw_text:
                self.logger.warning(f"Could not find or parse '{stat_label}' for fighter: {name}")
                return None

            return raw_text.split(":")[1].strip()

        item["height"] = get_stat("Height")
        item["weight"] = get_stat("Weight")
        item["dob"] = get_stat("DOB")
        item["reach"] = get_stat("Reach")
        item["stance"] = get_stat("STANCE")
        item["SLpM"] = get_stat("SLpM")
        item["SS_acc"] = get_stat("Str. Acc.")
        item["SS_def"] = get_stat("Str. Def")
        item["SApM"] = get_stat("SApM")
        item["TD_avg"] = get_stat("TD Avg.")
        item["TD_acc"] = get_stat("TD Acc.")
        item["TD_def"] = get_stat("TD Def.")
        item["sub_avg"] = get_stat("Sub. Avg.")

        yield item













