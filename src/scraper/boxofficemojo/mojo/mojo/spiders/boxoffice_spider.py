import scrapy
import pandas as pd
from ..items import MojoItem

class MojoSpider(scrapy.Spider):

    name="mojo"
    query_url = "https://www.boxofficemojo.com/search/?q="
    data = pd.read_csv('batch/megaset-batch-16.csv')
    movies = pd.DataFrame(data)
    #movies = ['on the road', 'ewewewew', 'me and orson welles']
    queries = []
    for index, row in movies.iterrows():
        movie_name = row['Name'].replace(' ', '+')
        query = query_url + movie_name
        print(query)
        queries.append(query)
    start_urls = queries

    def parse(self, response):
        link = response.xpath('//*[@id="a-page"]/main/div/div/div/div/div/div[2]/a/@href')
        #link = row.xpath('./td[2]/a/@href')
        #print(link)
        try:
            url = response.urljoin(link[0].extract())
            print('good_link')
            print(url)
            yield scrapy.Request(url, self.parse_link)
        except:
            print("Bad link")

    def parse_link(self, response): 
        item = MojoItem()
        movie_title =''
        movie_domestic = ''
        movie_international = ''
        movie_year = ''
        budget = ''
        runtime = ''
        rating = ''
        genres = ''

        movie_title = response.xpath('//*[@id="a-page"]/main/div/div/div/div/div/div[2]/div/h1/text()')[0].extract()
        try:
            movie_domestic = response.xpath('//*[@id="a-page"]/main/div/div[3]/div/div/div/span[2]/span/text()')[0].extract()
        except:
            pass
            print('No domestic')
        try:
            movie_international = response.xpath('//*[@id="a-page"]/main/div/div[3]/div/div/div[2]/span[2]/span/text()')[0].extract()
        except:
            pass
            print('No international')

        movie_year = response.xpath('//*[@id="a-page"]/main/div/div/div/div/div/div[2]/div/h1/span/text()')[0].extract()
        
        for i in range(9):
            s = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[' + str(i+1) + ']/span/text()'
            s2 = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[' + str(i+1) + ']/span[2]/text()'
            s3 = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[' + str(i+1) + ']/span[2]/span/text()'
            try: 
                current_field = response.xpath(s)[0].extract()
                current_field = str(current_field.replace(" ", ""))
                print(current_field)
            except:
                break
            if(current_field == 'MPAA'):
                print('FOUND ONEEEEEEEE')
            if (current_field == 'Budget' or current_field == 'RunningTime' or current_field == 'MPAA' or current_field == 'Genres'):
                print('Looking')
                if (current_field == 'Budget'):
                    print('Detected BUDGET')
                    try:
                        budget = response.xpath(s3)[0].extract()
                    except:
                        budget = response.xpath(s2)[0].extract()
                if (current_field == 'RunningTime'):
                    print('Detected RUNTIME')
                    try:
                        runtime = response.xpath(s2)[0].extract()
                    except:
                        runtime = response.xpath(s3)[0].extract()
                if (current_field == 'MPAA'):
                    print('Detected MPAA')
                    try:
                        rating = response.xpath(s2)[0].extract()
                    except:
                        rating = response.xpath(s3)[0].extract()
                if (current_field == 'Genres'):
                    print('Detected GENRES')
                    try:
                        genres = response.xpath(s2)[0].extract()
                    except:
                        genres = response.xpath(s3)[0].extract()
                    genres = genres.replace("\n", ";").replace(" ", '').replace(";;", ";")
            else:
                print('Skipping')
                continue
                


        print(f"The Movie Title is {movie_title}")
        print(f"The Domestic Revenue is {movie_domestic}")
        print(f"The Foreign Revenue is {movie_international}")
        print(f"The Movie Year is {movie_year}")
        print(f"The Movie Budget is {budget}")
        print(f"The runtime of the movie is {runtime}")
        print(f"The rating of the movie is {rating}")
        print(f"The genres of the movie is {genres}")

        item['title'] = movie_title
        item['year'] = movie_year
        item['domestic'] = movie_domestic
        item['foreign'] = movie_international
        item['budget'] = budget
        item['runtime'] = runtime
        item['rating'] = rating
        item['genre'] = genres

        yield item
