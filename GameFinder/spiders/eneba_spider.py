import scrapy


class EnebaSpider(scrapy.Spider):
  name = "eneba"

  def start_requests(self):
    game = getattr(self, "game", None)
    urls = [
      f"https://www.eneba.com/latam/store/games?page=1&regions[]=global&regions[]=latam&regions[]=colombia&text={game}&types[]=game"
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse,
                           cookies={"exchange": "COP", "region": "colombia"})

  def parse(self, response):
    priceTag = response.css(
        "main div div section div:nth-child(2) div:nth-child(2) div div div:nth-child(3)")

    titleTag = response.css(
        "main div div section div:nth-child(2) div:nth-child(2) div div div:nth-child(2)")

    for price, title in zip(priceTag, titleTag):
      value = price.css("a span span::text").get()
      title = title.css("div div span::text").get()

      yield {
        "title": title,
        "value": value
      }

# next = response.css("ul.rc-pagination li.rc-pagination-next").get()
