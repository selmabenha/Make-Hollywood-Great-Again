import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import concurrent.futures

MAX_THREADS = 30
df_wiki_to_scrape = pd.read_csv('wiki_scrape.csv')

def get_wiki_info(current_link):
    r = requests.get(current_link['link'])
    index = current_link['index']
    soup = BeautifulSoup(r.text, 'html.parser')
    info_table = soup.find('table', class_='infobox vevent')
    try:
        tr = info_table.find_all('tr')
        for i in range(len(tr)):
        #print(tr[i].text)
            if ("Country" in tr[i].text):
                country = tr[i].text.replace('Country', '')
                #print(country)
                df_wiki_to_scrape.loc[index, 'Countries'] = country.lower()
            elif ("Countries" in tr[i].text):
                country = tr[i].text.replace('Countries', '').replace('\n', '')
                #print(country)
                df_wiki_to_scrape.loc[index, 'Countries'] = country.lower()
            elif ("Languages" in tr[i].text):
                language = tr[i].text.replace('Languages', '').replace('\n', '')
                #print(language)
                df_wiki_to_scrape.loc[index, 'Languages'] = language.lower()
                continue
            elif ("Language" in tr[i].text):
                language = tr[i].text.replace('Language', '')
                #print(language)
                df_wiki_to_scrape.loc[index, 'Languages'] = language.lower()
    except:
        pass

def get_links():
    all_links = []
    init_link = 'https://en.wikipedia.org/wiki/'
    for index, row in df_wiki_to_scrape.iterrows():
        current_name = row['Name']
        current_name = current_name.title().replace(" ", "_")
        current_link = init_link + current_name
        current = {'index': index,
                    'link': current_link}
        all_links.append(current)
    return all_links


def main():
    links = get_links()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        movies = executor.map(get_wiki_info, links)
    #scraped_df = pd.DataFrame(movies)
    df_wiki_to_scrape.to_csv('wiki2.csv', index=False)

if __name__ == "__main__":
    main()

