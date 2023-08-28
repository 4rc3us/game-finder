class XboxUrlBuilder:
    def __init__(self, base_address):
        self.base_address = base_address
        self.platforms = []
        self.separator = "%2C"
        self.params = []
    
    def add_platforms(self, platforms: str):
        platforms = platforms.split(",")
        self.platforms.extend(map(lambda platform: self.handle_platform(platform), platforms))
        
        return self
    
    def add_game(self, game: str = None):
        if game:
            self.params.append(f"q={game}")
        
        return self
    
    def build(self):
        params = "&".join(self.params)
        return f"{self.base_address}?{params}"
    
    @staticmethod
    def handle_platform(platform: str):
        platform = platform.strip().lower()
        
        match platform:
            case "xboxone":
                return "XboxOne"
            case "xboxseriesx":
                return "XboxSeriesX%7CS"
            case "xboxseriesx|s":
                return "XboxSeriesX%7CS"
            case "xboxseriess":
                return "XboxSeriesX%7CS"
            case "xboxseries":
                return "XboxSeriesX%7CS"
            case "pc":
                return "PC"
