import scrapy

from GameFinder.Builders.XboxUrlBuilder import XboxUrlBuilder
from GameFinder.items import GameItem


def normalize_price(price: str):
    if price is None:
        return "0"
    
    value = price.replace(",", "").replace("$", "").replace(".", "").strip()
    if value.isdigit():
        return value
    
    return "0"


class XboxSpider(scrapy.Spider):
    name = "xbox"
    base_address = "https://www.xbox.com/es-CO/search"
    game = None
    
    def start_requests(self):
        self.game = getattr(self, "game", None)
        platforms = getattr(self, "platforms", None)
        
        builder = XboxUrlBuilder(self.base_address)
        
        url = builder.add_game(self.game).build()
        
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        body = response.css("body")
        context_search = body.css("#primaryArea div div div")
        games = context_search.css("div:nth-child(3) section")
        
        for game in games:
            game_item = GameItem()
            game_title = game.css("span.x-heading::text").get()
            game_photo = 'http:' + game.css("img.c-image::attr(src)").get()
            game_price = game.css("div.x-price span::text").get()
            game_url = game.css("a::attr(href)").get()
            
            game_item["title"] = game_title
            game_item["price"] = normalize_price(game_price)
            game_item["link"] = game_url
            game_item["store"] = "xbox"
            game_item["photo"] = game_photo
            game_item["exchange"] = "COP"
            
            yield game_item
