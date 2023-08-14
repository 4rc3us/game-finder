import json
import unicodedata

import scrapy

from GameFinder.Builders.XboxUrlBuilder import XboxUrlBuilder
from GameFinder.items import GameItem


class XboxSpider(scrapy.Spider):
    name = "xbox"
    base_address = "https://www.xbox.com/es-CO/search/results/games"
    game = None
    
    def start_requests(self):
        self.game = getattr(self, "game", None)
        platforms = getattr(self, "platforms", "xboxseries")
        
        builder = XboxUrlBuilder(self.base_address)
        
        url = builder.add_platforms(platforms).add_game(self.game).build()
        
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        game_data = response.css("head script::text").get().strip()
        results_list = self.find_json(game_data)["core2"]["products"]["productSummaries"]
        
        for game in results_list:
            game_title = game["title"]
            game_sku = game["specificPrices"]["purchaseable"][0]["skuId"]
            game_id = game["productId"]
            game_photos = [{"url": img["url"], "width": img["width"], "height": img["height"]}
                           for img in game["images"].values()]
            
            game_item = GameItem()
            game_item["title"] = game_title
            game_item["price"] = game["specificPrices"]["purchaseable"][0]["listPrice"]
            game_item["link"] = self.build_game_link(game_title, game_id, game_sku)
            game_item["store"] = "xbox"
            game_item["photos"] = game_photos
            game_item["exchange"] = "COP"
            
            yield game_item
    
    @staticmethod
    def find_json(text: str):
        start_index = text.find('{')
        end_index = text.find('};', start_index) + 1
        json_string = text[start_index:end_index]
        
        data = json.loads(json_string)
        product_summaries = [value for value in data["core2"]["products"]["productSummaries"].values()]
        data["core2"]["products"]["productSummaries"] = product_summaries
        
        return data
    
    @staticmethod
    def build_game_link(game_title: str, game_id: str, sku_id: str):
        normalized_text = unicodedata.normalize('NFKD', game_title).encode('ascii', 'ignore').decode('utf-8')
        return f"https://www.xbox.com/es-CO/games/store/{normalized_text.replace(' ', '-')}/{game_id}/{sku_id}"
