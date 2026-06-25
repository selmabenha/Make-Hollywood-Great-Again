import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import concurrent.futures

MAX_THREADS = 30

def get_links_on_page(page):
    r = requests.get('https://www.the-numbers.com/movie/budgets/all' + page)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = soup.find_all('a')
    valid_links = []
    counter = 0
    init_link = 'https://www.the-numbers.com'
    for link in all_links:
        if(link.get('href') and not  link.get('href').startswith('/movie/budgets')\
            and link.get('href').startswith('/movie/') and counter < 100):
            #print(link.get('href'))
            valid_links.append(init_link + link.get('href'))
            counter+=1

    return valid_links

def get_movie_info(soup_movie):
    current_movie = {'Name' : '',
                    'Year' : '',
                    'Languages' : '',
                    'Countries': '',
                    'Genres': '',
                    'Budget': '',
                    'runtime': '',
                    'rating': '',
                    'domestic_gross': '',
                    'foreign_gross': '',
                    'worldwide_gross': '',
                    }
    movie_title_with_year = soup_movie.find('h1').text
    year = movie_title_with_year[movie_title_with_year.find("(")+1:movie_title_with_year.find(")")]
    movie_title = movie_title_with_year[:movie_title_with_year.find("(")]

    current_movie['Name'] = movie_title
    current_movie['Year'] = year

    all_td = soup_movie.find_all('td')
    for i in range(len(all_td)):
        if all_td[i].find('b'): 
            if all_td[i].find('b').text=='Production Countries:':
                current_movie['Countries'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Domestic Box Office':
                current_movie['domestic_gross'] = all_td[i+1].text
            elif all_td[i].find('b').text=='International Box Office':
                current_movie['foreign_gross'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Worldwide Box Office':
                current_movie['worldwide_gross'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Running Time:':
                current_movie['runtime'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Genre:':
                current_movie['Genres'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Languages:':
                current_movie['Languages'] = all_td[i+1].text
            elif all_td[i].find('b').text=='MPAA Rating:':
                current_movie['rating'] = all_td[i+1].text
            elif all_td[i].find('b').text=='Production Budget:':
                current_movie['Budget'] = all_td[i+1].text
            
    return current_movie

def task(link):
    r_movie = requests.get(link)
    soup_movie = BeautifulSoup(r_movie.text, 'html.parser')
    movie = get_movie_info(soup_movie)
    return movie

def main():
    start = 21 
    pages_to_scrape = 66 - start
    for i in range(start, start+pages_to_scrape):
        if i == 0:
            page=''
            filename = "/0"
        else:
            page = '/' + str(i*100 + 1)
            filename = page
        links = get_links_on_page(page)
        print('got all links')
        #all_movies_info = []
        print("For batch : " + filename)
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            movies = tqdm(executor.map(task, links), total=len(links))
            #all_movies_info.append(movie)
        scraped_df = pd.DataFrame(movies)
        scraped_df.to_csv('scraped_data'+filename+".csv", index=False)

if __name__ == "__main__":
    main()