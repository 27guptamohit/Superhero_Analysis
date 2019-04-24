import requests
import lxml.html
import pandas as pd
from time import sleep



def get_earnings() -> lxml.etree:




    url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_superhero_films'


    # Fetching the url web page, and converting the response into an HTML document tree:
    tree = None
    while tree is None:
        try:
            r = requests.get(url)
            print("The request was successful")
            tree = lxml.html.fromstring(r.content)
            break
        except (ConnectionError, ConnectionRefusedError):
            print('The request was unsuccessful. Retrying in 5 seconds...')
            sleep(5)
    return tree

tree = get_earnings()

Rank = []
Film = []
Worldwide_Gross = []
Year = []
Superhero = []
Source = []

for i in list(range(2,52)):

    rank_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[1]/text()"
    Rank.append(tree.xpath(rank_url))

    film_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[2]/i/a/text()"
    Film.append(tree.xpath(film_url))


    gross_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[3]/text()"
    Worldwide_Gross.append(tree.xpath(gross_url))

    year_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[4]/text()"
    Year.append(tree.xpath(year_url))


    name_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[5]/a/text()"
    Superhero.append(tree.xpath(name_url))

    source_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[6]/a/text()"
    if tree.xpath(source_url) != []:
        Source.append(tree.xpath(source_url))
    elif "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[6]/a/text()" == []:
        Source.append(tree.xpath("//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr["+ str(i) + "]/td[6]/a/text()"))





print(len(Rank))

print(Rank[0:5])

print(len(Film))

print(Film[0:5])

print(len(Worldwide_Gross))

print(Worldwide_Gross[0:5])

print(len(Year))

print(Year[0:5])

print(len(Superhero))

print(Superhero[0:5])

print(len(Source))

print(Source[0:5])



















