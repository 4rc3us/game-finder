class EnebaUrlBuilder:
    def __init__(self, base_address):
        self.base_address = base_address
        self.params = []
    
    def add_platforms(self, platforms):
        platforms = platforms.split(",")
        platforms = list(map(lambda platform: f"drms[]={platform}", platforms))
        self.params.append("&".join(platforms))
        return self
    
    def add_regions(self, regions):
        regions = regions.split(",")
        regions = list(map(lambda region: f"regions[]={region}", regions))
        self.params.append("&".join(regions))
        return self
    
    def add_game(self, game):
        if game:
            self.params.append(f"text={game}")
        
        return self
    
    def build(self):
        params = "&".join(self.params)
        return f"{self.base_address}/latam/store/games?{params}&page=1&types[]=game"
