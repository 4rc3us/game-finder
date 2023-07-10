import scrapy

from GameFinder.Builders.EnebaUrlBuilder import EnebaUrlBuilder


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
                             cookies={"exchange": "COP", "region": "colombia"})
    
    def parse(self, response, **kwargs):
        main_game_container = response.css(
            "main div div section div.JZCH_t div.pFaGHa")
        
        for game in main_game_container:
            game_title = game.css(
                "div:nth-child(2) div div:first-child span::text").get()
            
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
            
            yield {
                "title": game_title,
                "value": game_price,
                "link": game_url
            }
        
        # avoid pagination if game is specified
        if self.game:
            return
        
        next_page = response.css("ul.rc-pagination li.rc-pagination-next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def get_blacklist(self):
        return getattr(self, "blacklist", "").split(",")
