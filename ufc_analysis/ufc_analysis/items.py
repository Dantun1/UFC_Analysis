import scrapy


class FighterItem(scrapy.Item):
    name = scrapy.Field()
    nickname = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    dob = scrapy.Field()
    reach = scrapy.Field()
    stance = scrapy.Field()
    record = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    SLpM = scrapy.Field()
    SS_acc = scrapy.Field()
    SS_def = scrapy.Field()
    SApM = scrapy.Field()
    TD_avg= scrapy.Field()
    TD_acc = scrapy.Field()
    TD_def = scrapy.Field()
    sub_avg = scrapy.Field()

