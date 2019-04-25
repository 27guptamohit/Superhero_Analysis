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

marvel_DC_earnings_df = boxoffice_df.merge(wiki_df, on="Title")

# As "Incredibles 2" and "Teenage Mutant Ninja Turtles" are not from DC and Marvel, we need to omit them from the results.



# I learnt the below code from the below link. It stores the string that we do not want in our dataframe and
# then it removes the whole row where it finds the given string.
# https://stackoverflow.com/questions/28679930/how-to-drop-rows-from-pandas-data-frame-that-contains-a-particular-string-in-a-p
# Comment number 14

searchfor = ['Incredibles 2', 'Teenage Mutant Ninja Turtles']
marvel_DC_earnings_df = marvel_DC_earnings_df[~marvel_DC_earnings_df.Title.str.contains('|'.join(searchfor))]


# The two production houses are having contracts with below studio:
# Marvel = BV, Sony, Fox, Par.
# DC Comics = WB

marvel_DC_earnings_df['Publisher'] = np.where(marvel_DC_earnings_df['Studio'] == 'WB', 'DC Comics', 'Marvel Comics')






def fivethirtyeight_df(fte_file: str, publisher: str):

    dc_fte = pd.read_csv(fte_file,
                         usecols=['name', 'ID', 'ALIGN', 'EYE', 'HAIR', 'SEX', 'ALIVE', 'APPEARANCES'])

    # I learnt below regex code to extract what ever is in bracket from below link
    # https://stackoverflow.com/questions/16842001/copy-text-between-parentheses-in-pandas-dataframe-column-into-another-column

    dc_fte['Real Name'] = dc_fte['name'].str.extract('.*\((.*)\).*')

    # https://stackoverflow.com/questions/20894525/how-to-remove-parentheses-and-all-data-within-using-pandas-python

    dc_fte['name'] = dc_fte['name'].str.replace(r"\(.*\)", "")

    dc_fte['Publisher'] = publisher

    # I have learnt to use the rstrip from the comment 3 of below link:
    # https://stackoverflow.com/questions/51778480/remove-certain-string-from-entire-column-in-pandas-dataframe


    dc_fte['ID'] = dc_fte['ID'].str.rstrip('Identity')

    dc_fte['ALIGN'] = dc_fte['ALIGN'].str.rstrip('Characters')

    dc_fte['EYE'] = dc_fte['EYE'].str.rstrip('Eyes')

    dc_fte['HAIR'] = dc_fte['HAIR'].str.rstrip('Hair')

    dc_fte['SEX'] = dc_fte['SEX'].str.rstrip('Characters')

    dc_fte['ALIVE'] = dc_fte['ALIVE'].str.rstrip('Characters')

    dc_fte.rename(columns={'name': 'Superhero Name',
                           'ID': 'Identity',
                           'ALIGN': 'Alignment',
                           'EYE': 'Eye Color',
                           'HAIR': 'Hair Color',
                           'SEX': 'Gender',
                           'ALIVE': 'Alive',
                           'APPEARANCES': 'Appearances'}, inplace=True)

    return dc_fte



dc_marvel_fte1 = fivethirtyeight_df('1fte.csv', 'DC')

dc_marvel_fte2 = fivethirtyeight_df('2fte.csv', 'Marvel')

dc_marvel_fte_df = pd.concat([dc_marvel_fte1, dc_marvel_fte2])


def marvel_big_data(a:str = "1c.csv", b:str = "2c.csv"):
    df1 = pd.read_csv(a,
                      usecols=['Name', 'Intelligence', 'Strength', 'Speed',
                               'Durability', 'Power', 'Combat', 'Total'])

    df2 = pd.read_csv(b,
                      usecols=['ID', 'Name', 'Alignment', 'Gender', 'Race',
                               'Publisher', 'Height', 'Weight'])

    df3 = pd.merge(df1, df2, on='Name', how='inner')

    df3['Alignment'] = df3['Alignment'].str.title()

    return df3


marvel_big_data_df = marvel_big_data()






















