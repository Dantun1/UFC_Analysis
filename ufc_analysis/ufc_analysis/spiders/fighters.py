import scrapy
import string

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
        name = response.css(".b-content__title-highlight::text").get()
        self.logger.info(f"Parsing fighter: {name}")






