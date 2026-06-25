# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class MojoPipeline:
    def __init__(self):
        self.csvwriter = csv.writer(open("batch16.csv", "w", newline=''))
        self.csvwriter.writerow(['Name', 'Year', 'Domestic', 'Foreign', 'Budget', 'Runtime', 'Rating', 'Genre'])

    def process_item(self, item, spider):
        row = []
        row.append(item["title"])
        row.append(item["year"])
        row.append(item["domestic"])
        row.append(item["foreign"])
        row.append(item['budget'])
        row.append(item['runtime'])
        row.append(item['rating'])
        row.append(item['genre'])
        self.csvwriter.writerow(row)
        return item
    
    def close_spider(self, spider):
        print("Done")
