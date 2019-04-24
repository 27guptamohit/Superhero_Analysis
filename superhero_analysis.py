import requests
import lxml.html
import pandas as pd
from time import sleep
import numpy as np



def get_earnings(url) -> lxml.etree:


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



boxofficemoio_url = 'https://www.boxofficemojo.com/genres/chart/?id=superhero.htm'




boxoffice_tree = get_earnings(boxofficemoio_url)

def boxoffice_data(boxoffice_tree):

    Title = boxoffice_tree.xpath("//tr/td[2]/font/a/b/text()")
    Title = list(map(str, Title))

    Studio = boxoffice_tree.xpath("//tr/td[3]/font/a/text()")
    Studio = list(map(str, Studio[1:101]))

    Gross_Income = boxoffice_tree.xpath("//tr/td[4]/font/b/text()")
    Gross_Income = list(map(str, Gross_Income))

    df = pd.DataFrame(list(zip( Title, Gross_Income, Studio)), columns=['Title', 'Gross Income', 'Studio'])

    df['Gross Income'] = [x.strip('$') for x in df['Gross Income']]
    df['Gross Income'] = [x.replace(',', '') for x in df['Gross Income']]
    df['Gross Income'] = df['Gross Income'].astype('int64')

    return df

boxoffice_df = boxoffice_data(boxoffice_tree)


wiki_url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_superhero_films'

wiki_tree = get_earnings(wiki_url)



def wiki_data(wiki_tree):
    Film = []

    for i in list(range(2, 52)):
        film_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr[" + str(i) + "]/td[2]/i/a/text()"
        Film = Film + wiki_tree.xpath(film_url)
        Film = list(map(str, Film))

    df = pd.DataFrame((Film), columns=['Title'])

    return df


wiki_df = wiki_data(wiki_tree)


# Now I am merging the two data frames to filter the DC and Marvel only movies

marvel_DC_df = boxoffice_df.merge(wiki_df, on="Title")

# As "Incredibles 2" and "Teenage Mutant Ninja Turtles" are not from DC and Marvel, we need to omit them from the results.



# I learnt the below code from the below link. It stores the string that we do not want in our dataframe and
# then it removes the whole row where it finds the given string.
# https://stackoverflow.com/questions/28679930/how-to-drop-rows-from-pandas-data-frame-that-contains-a-particular-string-in-a-p
# Comment number 14

searchfor = ['Incredibles 2', 'Teenage Mutant Ninja Turtles']
marvel_DC_df = marvel_DC_df[~marvel_DC_df.Title.str.contains('|'.join(searchfor))]


# The two production houses are having contracts with below studio:
# Marvel = BV, Sony, Fox, Par.
# DC Comics = WB

marvel_DC_df['Producers'] = np.where(marvel_DC_df['Studio'] == 'WB', 'DC', 'Marvel')


















