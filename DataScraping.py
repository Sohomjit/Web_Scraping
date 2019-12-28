from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
url = "https://www.imdb.com/search/title?groups=best_picture_winner&sort=year,desc&count=100&view=advanced"

uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')
oscar_film_records = []

for div in page_soup.find_all("div", attrs={"class", "lister-item-content"}):

    film_name = (div.find('a').contents[0])
    runtime = div.find('span', {'class': 'runtime'})
    runtime_temp = runtime.text[:-3]
    runtime_temp = int(runtime_temp)
    rating = div.find('strong').contents[0]
    rating_temp = rating
    rating_temp = float(rating_temp)
    total_year_list = div.find('span', {'class': 'lister-item-year text-muted unbold'})
    year_temp = total_year_list.text[1:-1]
    if len(year_temp) > 4:
       year_temp = year_temp[4:]
       year_temp = int(year_temp)
    else:
        year_temp = int(year_temp)

    votes_list = div.find_next('p', {'class': 'sort-num_votes-visible'}).contents[3]
    votes_list_temp = votes_list.text
    votes_list_temp = votes_list_temp.replace(',', '')
    votes_list_temp = int(votes_list_temp)

    meta_score = div.find('div', {'class': 'inline-block ratings-metascore'})
    if meta_score:
        meta_scores = meta_score.text
        m_score = meta_scores[:4].strip()
        m_score = float(m_score)

    else:
        m_score = float(m_score)
        m_score = 0

    gross_value = div.find_next('p', {'class': 'sort-num_votes-visible'})
    g1_value = div.find_next('span', {'name': 'nv'})
    g2_value = g1_value.find_next_sibling('span', {'name': 'nv'})

    if g2_value:
        gross_temp = g2_value.text[1:-1]
        gross_temp = float(gross_temp)

    else:
        gross_temp = 0.0

    admit_value = div.find_next('span', {'class': 'certificate'})
    if admit_value:
        cert = admit_value.text

    else:
        cert = "NA"

    film_data_tuple = (film_name, cert, runtime_temp, rating_temp,m_score, year_temp, votes_list_temp, gross_temp)
    oscar_film_records.append(film_data_tuple)


print("========")
print("Process Completed Total Records Displayed Below ======")
print("========")
print(len(oscar_film_records))

#for onetuple in oscar_film_records:
#    print("\n")
#    for elements in onetuple:
#        print(elements)

df = pd.DataFrame(oscar_film_records, columns=['film_name', 'certificate', 'runtime', 'star_rating', 'metascore', 'year', 'votes', 'Gross'])
df.to_csv('oscar_list.csv', encoding='utf-8', index=False)
