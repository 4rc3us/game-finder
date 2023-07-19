import argparse

parser = argparse.ArgumentParser(prog="gamefinder", description="Scrapper to find games")
parser.add_argument("game")

args = parser.parse_args()

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    process = CrawlerProcess(get_project_settings())
    
    process.crawl("eneba", game=args.game, platforms="xbox", regions="global,colombia,latam",
                  blacklist="argentina")
    process.crawl("xbox", game=args.game)
    
    process.start()
