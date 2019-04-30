

import requests
import lxml.html
import pandas as pd
from time import sleep
import numpy as np



def get_earnings(url) -> lxml.etree:
    """
    The function is used to import the input url parameter to convert it into a  html document tree.
    :param url: The url of the webpage that I want to convert into HTML document tree.
    :return: The object returned is an lxml etree

    >>> boxofficemoio_url = 'https://www.boxofficemojo.com/genres/chart/?id=superhero.htm'
    >>> type(get_earnings(boxofficemoio_url))
    The request was successful
    <class 'lxml.html.HtmlElement'>

    """



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


wiki_url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_superhero_films'

wiki_tree = get_earnings(wiki_url)

#=================================================



def boxoffice_data(boxoffice_tree):
    """
    The function is used to scrape the earnings and movie name data from the boxofficemojo website.
    I only extracted the Title of the movie, the studio who produced it and the gross income of the movie.
    I also removed the '$' and ',' symbols from the earnings data and also changed the data type for future analysis.

    :param boxoffice_tree:  This is the
    :return: I am returning the resultant data frame in this function.

    >>> boxoffice_df = boxoffice_data(boxoffice_tree)
    >>> print(type(boxoffice_df))
    <class 'pandas.core.frame.DataFrame'>
    """

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


#=================================================



def wiki_data(wiki_tree):
    """
    The function extracts the name of the movies only from the Marvel and DC comics. The previous
    function from the boxofficemojo only extracted the name of the movies with all the different
    production houses apart from the Marvel and DC comics.

    Publishing house: Marvel, DC
    Production house: Sony, Fox Studios, BV, Warner Bros

    Marvel have contracts with different production houses thus, I would link the wiki data with the boxofficemojo
    data in order to identify the linked publishing house.

    :param wiki_tree: This returns the name of the movies only from the Marvel and DC comics.
    :return: This returns data frame

    >>> wiki_df = wiki_data(wiki_tree)
    >>> print(type(wiki_df))
    <class 'pandas.core.frame.DataFrame'>
    """
    Film = []

    for i in list(range(2, 52)):
        film_url = "//*[@id='mw-content-text']/div/table[1]/tbody[1]/tr[" + str(i) + "]/td[2]/i/a/text()"
        Film = Film + wiki_tree.xpath(film_url)
        Film = list(map(str, Film))

    df = pd.DataFrame((Film), columns=['Title'])

    return df


wiki_df = wiki_data(wiki_tree)



#=================================================


# Now I am merging the two data frames to filter the DC and Marvel only movies

earnings_df = boxoffice_df.merge(wiki_df, on="Title")

# As "Incredibles 2" and "Teenage Mutant Ninja Turtles" are not from DC and Marvel, we need to omit them from the results.
# I learnt the below code from the below link. It stores the string that we do not want in our dataframe and
# then it removes the whole row where it finds the given string.
# https://stackoverflow.com/questions/28679930/how-to-drop-rows-from-pandas-data-frame-that-contains-a-particular-string-in-a-p
# Comment number 14

searchfor = ['Incredibles 2', 'Teenage Mutant Ninja Turtles']
earnings_df = earnings_df[~earnings_df.Title.str.contains('|'.join(searchfor))]


# The two production houses are having contracts with below studio:
# Marvel = BV, Sony, Fox, Par.
# DC Comics = WB

earnings_df['Publisher'] = np.where(earnings_df['Studio'] == 'WB', 'DC Comics', 'Marvel Comics')


#====================================================================================



def fivethirtyeight_df(fte_file: str, publisher: str):
    """
    I am using this function to clean the data downloaded from fivethirtyeight kaggle link.
    I am only keeping the relevant columns and cleaning the multiple column's data in order to use it for analysis.
    I am also adding new columns in order to do the data analysis.

    :param fte_file: The downloaded file that I am taking as the input.
    :param publisher: Name of the publisher whose characters are in the mentioned data.
    :return: It returns the cleaned and reformated data frame.

    >>> dc_marvel_fte1 = fivethirtyeight_df('1fte.csv', 'DC')
    >>> print(type(dc_marvel_fte1))
    <class 'pandas.core.frame.DataFrame'>

    """

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

    dc_fte['name'] = dc_fte['name'].str.strip()

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



dc_marvel_fte1 = fivethirtyeight_df('1fte.csv', 'DC Comics')

dc_marvel_fte2 = fivethirtyeight_df('2fte.csv', 'Marvel Comics')


# Concating the two dataframes obtained on the basis of column names.


comics_df = pd.concat([dc_marvel_fte1, dc_marvel_fte2])

comics_df.drop_duplicates(subset ="Superhero Name",
                          keep = "first", inplace = True)


#=====================================================================================

def marvel_big_data(a:str = "1c.csv", b:str = "2c.csv"):
    """
    Function to accept the two data sets downloaded form the Marvel_DC kaggle link and set it as default.
    If no other parameters are entered, the default parameters would be taken as the input.
    :param a: File 1 which contains the details about the superhero's characteristic powers
    :param b: File 2 which contains the details about the race, height, weight, publisher
    :return: It returns the merged data frame

    >>> marvel_big_data_df = marvel_big_data()
    >>> print(type(stats_df))
    <class 'pandas.core.frame.DataFrame'>

    """
    df1 = pd.read_csv(a,
                      usecols=['Name', 'Intelligence', 'Strength', 'Speed',
                               'Durability', 'Power', 'Combat', 'Total'])

    df2 = pd.read_csv(b,
                      usecols=[ 'Name', 'Race',
                                'Height', 'Weight','Publisher'])


    df3 = pd.merge(df1, df2, on='Name', how='inner')

    df3['Name'] = df3['Name'].str.strip()
    df3['Race'] = np.where(df3['Race'] == 'Human', 'Human', 'Mutant')

    df3.rename(columns = {'Name': 'Superhero Name'}, inplace=True)

    # Filtering the rows which have the DC and Marvel as publishers
    df3 =  df3[(df3['Publisher']  == "Marvel Comics")|(df3['Publisher']  == "DC Comics") ]

    # Now droping the publishers column
    df3.drop(['Publisher'], axis=1)


    return df3


stats_df = marvel_big_data()


stats_df.drop_duplicates(subset ="Superhero Name",
                         keep = "first", inplace = True)


#=============================================================


# Below, the validate parameter in the merge function validates the many to many relationship in more than one entries are present
# in both the tables.

final_merged_df = pd.merge(stats_df, comics_df, on=['Superhero Name'], how='inner', validate='m:m')

#=============================================================






























