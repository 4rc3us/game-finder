import re

import scrapy

from GameFinder.Builders.EnebaUrlBuilder import EnebaUrlBuilder
from GameFinder.items import GameItem


class EnebaSpider(scrapy.Spider):
    name = "eneba"
    
    base_address = "https://www.eneba.com"
    game = None
    
    def start_requests(self):
        self.game = getattr(self, "game", None)
        platforms = getattr(self, "platforms", "xbox")
        regions = getattr(self, "regions", "global")
        
        builder = EnebaUrlBuilder(self.base_address)
        
        url = builder.add_platforms(platforms).add_regions(regions).add_game(self.game).build()
        yield scrapy.Request(url=url, callback=self.parse,
                             cookies={"exchange": "COP", "region": regions})
    
    def parse(self, response, **kwargs):
        main_game_container = response.css(
            "main div div section div.JZCH_t div.pFaGHa")
        
        for game in main_game_container:
            game_item = GameItem()
            game_title = game.css(
                "div:nth-child(2) div div:first-child span::text").get()
            
            game_photos = game.css(
                "div:first-child div picture source::attr(srcset)").getall()
            
            price_section = game.css(
                "div:nth-child(3) a")
            
            game_price = price_section.css("div:first-child span span::text").get()
            
            # avoid blacklisted words
            if any(word in game_title.lower() for word in self.get_blacklist()):
                continue
            
            # avoid null price
            if not game_price:
                continue
            
            game_url = f"{self.base_address}{price_section.css('::attr(href)').get()}"
            
            game_item["title"] = game_title
            game_item["price"] = normalize_price(game_price)
            game_item["link"] = game_url
            game_item["store"] = "eneba"
            game_item["photo"] = process_pictures(game_photos)[2]
            game_item["exchange"] = "COP"
            
            yield game_item
        
        # avoid pagination if game is specified
        if self.game:
            return
        
        next_page = response.css("ul.rc-pagination li.rc-pagination-next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def get_blacklist(self):
        black_list = getattr(self, "blacklist", None)
        
        if not black_list:
            return []
        
        return black_list.split(",")


def process_pictures(pictures):
    new_list = []
    for item in pictures:
        links = re.findall(r'(https?://\S+)', item)
        
        new_list.extend(build_image(links))
    return new_list


def build_image(img):
    images = []
    for url in img:
        images.append(url)
    
    return images


def normalize_price(price):
    return price.replace("$", "").replace(",", "").replace(".", "").replace("COP", "").strip()
