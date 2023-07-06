import scrapy


class EnebaSpider(scrapy.Spider):
    name = "eneba"
    
    base_address = "https://www.eneba.com"
    
    def start_requests(self):
        game = getattr(self, "game", None)
        platforms = getattr(self, "platforms", "xbox")
        platforms = platforms.split(",")
        
        platforms = list(map(lambda platform: f"drms[]={platform}", platforms))
        platforms = "&".join(platforms)
        
        urls = [
            f"{self.base_address}/latam/store/games?{platforms}&page=1&regions[]=global&regions[]=latam&regions["
            f"]=colombia&text={game}&types[]=game"
        ]
        
        # https://www.eneba.com/latam/store/games?page=1&regions[]=global&regions[]=latam&regions[]=colombia&text=cyber&types[]=game
        
        # https://www.eneba.com/latam/store/games?drms[]=xbox&page=1&regions[]=global&regions[]=latam&regions[]=colombia&text=cyber&types[]=game
        
        for url in urls:
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
            
            if any(word in game_title.lower() for word in self.get_blacklist()):
                continue
            
            game_url = f"{self.base_address}{price_section.css('::attr(href)').get()}"
            
            yield {
                "title": game_title,
                "value": game_price,
                "link": game_url
            }
    
    def get_blacklist(self):
        return getattr(self, "blacklist", "").split(",")

# next = response.css("ul.rc-pagination li.rc-pagination-next").get()
