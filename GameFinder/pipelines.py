class OrderPipeline:
    def __init__(self):
        self.items = None
    
    def open_spider(self, spider):
        self.items = []
    
    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        self.items.sort(key=lambda x: x['title'])
        for item in self.items:
            print(item)