# Mohit Gupta, Superhero Analysis
# University of Illinois, Urbana-Champaign
# NetID: mohitg2
# Programming for Analytics & Data Processing (IS 590 PR)
# Spring 2019

# IMP:
# If you run this program for more than two many times, google will stop accepting your request and will mark your server as spam.
# Avoid running this program multiple times.
# More details can be found in this link:
# https://tools.ietf.org/html/rfc6585#page-3



# Please read the (Final Report.md) which contains the final conclusion of the project and whether the proposed hypothesis were true or not.
# Apart from the questions I proposed, my friends, co-workers and classmates(from IS 590 PR) were curious to know
# about few more details. So I am adding the questions they asked.


# Requirements of the project fulfilled :

#  1. Increased level of sophistication for Type II analysis
#  2. Linked 2+ datasets from distinct sources
#  3. Tested proposed hypothesis
#  4. Prior approval taken from instructor for project topic
#  5. Modified code on the basis of constructive feedback received from peers on "Presentation Day"
#  6. Included doctests and unit-tests with more than 85 % code coverage
#  7. All nine functions includes docstrings
#  8. Functions run with different input parameters without hard-coded vales (check def names_url() which generates output)
#     for the function (def get_tree()) as it's input.
#  9. Hypothesis testing & Conclusion mentioned in ( README.md )
# 10. Report from this program uploaded on Github (Superhero Report.txt)
# 11. Total lines of code: 600+




import requests
import lxml.html
import pandas as pd
from time import sleep
import numpy as np



def get_tree(url) -> lxml.etree:
    """
    The function is used to import the input url parameter to convert it into a  html document tree.
    :param url: The url of the webpage that I want to convert into HTML document tree.
    :return: The object returned is an lxml etree

    >>> boxofficemoio_url = 'https://www.boxofficemojo.com/genres/chart/?id=superhero.htm'
    >>> type(get_tree(boxofficemoio_url))
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

boxoffice_tree = get_tree(boxofficemoio_url)


wiki_url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_superhero_films'

wiki_tree = get_tree(wiki_url)

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

    df3.drop(['Publisher'], axis=1, inplace=True)

    return df3


stats_df = marvel_big_data()


stats_df.drop_duplicates(subset ="Superhero Name",
                         keep = "first", inplace = True)


#=============================================================


# Below, the validate parameter in the merge function validates the many to many relationship in more than one entries are present
# in both the tables.

final_merged_df = pd.merge(stats_df, comics_df, on=['Superhero Name'], how='inner', validate='m:m')
#=============================================================

# Answering the questions and hypothesis that I stated in the project proposal.

# Que 1.

# 1.a) Find six pairs of two characters who appeared most in comics(3 pairs Marvel + 3 Pairs DC)
# 1.b) Compare their combined power levels and check who wins.



sorted1 = final_merged_df.sort_values(['Publisher', 'Appearances'], ascending=[True, False])


# I extracted the characters with most comic appearances from both the Publishers.

ans1a = sorted1.groupby('Publisher').head(6).reset_index(drop=True, inplace=False)


# I will now make pairs with their combined power levels.
# I will pair them in the order of first and last from same publisher.
# For eg.
# Rank 1 with Rank 6, (DC)
# Rank 2 with Rank 5, (DC)
# Rank 3 with Rank 4, (DC)
# Rank 7 with Rank 12, (Marvel)
# Rank 8 with Rank 11, (Marvel)
# Rank 9 with Rank 10, (Marvel)


dc_dict = {}

for i in [0,6]:
    for j, k in zip(list(range(0,3)),list(range(5, 0, -2))):
        Name1 = ans1a['Superhero Name'][i+j]
        Name2 = ans1a['Superhero Name'][i+j+k]
        Name = Name1 + ' & ' + Name2 + ' ( ' + ans1a['Publisher'][i+j] + ' )'

        Total1 = ans1a['Total'][i+j]
        Total2 = ans1a['Total'][i + j+k]
        Total = Total1 + Total2

        dc_dict[Name] = Total




ans1b = pd.DataFrame(dc_dict.items(), columns=['Name', 'Combined Power']).sort_values(['Combined Power'], ascending=[False])



#================================



# Que 2. Marvel is not popular than DC Comics


# To answer this question, I have to perform several analysis.
# a. I will group the top 5 movies from Marvel and DC and check publishing house earned more.
# b. I will group all the movies from respective publishing house and
#    then check the total amount earned by both the publishing houses.


que2 = earnings_df.sort_values(['Publisher', 'Gross Income'], ascending=[True, False])

ans2a = que2.groupby('Publisher').head(5).reset_index(drop=True, inplace=False)
ans2a = ans2a.groupby('Publisher')['Gross Income'].sum()



ans2b = que2.groupby('Publisher')['Gross Income'].sum()




#==================================================

# Que 3. Are non-human superheros not more popular as compared to mutant superheros.


# a. I will find the count of number of human and mutant superheros for both the publishers.
# b. I will find the count of number of human and mutant superheros no matter who was their publisher.


ans3a = final_merged_df.groupby('Race').size()

ans3b = final_merged_df.groupby(['Publisher', 'Race']).size()


#==================================================


# Que 4. Finding the statistics of characters with different hair color, eye color, height and weight:


ans4 = comics_df.groupby(['Publisher', 'Eye Color','Hair Color']).size().nlargest(5)








#===========================================

# Que 5. Superheros with what hair color and eye color are more prone to live and die?



ans5 =  comics_df.groupby(['Alive', 'Eye Color', 'Hair Color']).size().nlargest(10)



#===========================================


# Que 6. What their race has to do with their Intelligence, Strength, Speed, Durability, Power, Combat, Total ?


ans6 = final_merged_df.groupby(['Publisher','Race'])['Intelligence','Strength', 'Speed','Durability' ,'Power' , 'Combat' ,'Total'].median()


#===============================================

# Que 7. How are height and weight distributed for characters in different publishing house?

ans7a = final_merged_df.groupby(['Publisher','Race'])['Height'].median()




ans7b = final_merged_df.groupby(['Publisher','Race'])['Weight'].median()

#================================================


# Trying to attempt complicated webscrapping:

# Que8 How many movie appearances does the characters with most comic appearances have?

# As, I do not have the movie appearances data readily, I had to perform a detailed web-scrapping again.



# First finding top four names of superheros from each production house with most comic appearances.


que2_names = list(sorted1.groupby('Publisher').head(4).reset_index(drop=True, inplace=False)['Superhero Name'])

def names_url(que2_names):
    """
    This function specifically searches google for the link of wikipedia which has details of superhero's movie appearances.
    A lot of factors went into consideration while designing this function.
    I had to manually design the search query "Superhero name" + " appearances in other media"
    as this is the only query which was returning me the link of wikipedia which mentions the list of movies the superhero
    appeared in.


    (Source)I learnt the below code to return link from search results from the below link:
    https://www.geeksforgeeks.org/performing-google-search-using-python-code/


    :param que2_names: List of superheros from Marvel and DC.
    :return: List of links which contains the superhero movie data.
    """
    names1_url = []

    for i in que2_names:
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")

        # to search
        query = i + " appearances in other media"

        for j in search(query, num=1, stop=1, pause=2):
            names1_url.append(str(j))

    return names1_url


names_url_list = names_url(que2_names)




def etree_data(etree, xpaths):
    """
    I will take the etree as the first parameter and input the xpath for the that wiki page as second parameter

    :param etree: Etree element for the referenced superhero
    :param xpaths: xpath of the desired data for specific superhero
    :return: count of number of movies by that superhero
    """

    movie_details = etree.xpath(xpaths)
    movie_details = list(map(str, movie_details))


    return len(movie_details)




names_etree_data = []

for i in names_url_list:
    names_etree_data.append(get_tree(i))

# I had to manually find the xpath of all the urls as the wikipedia tables were poorly designed.

xpath_sup = ["//tr[9]/td/div/ul/li//span/text()", "//tr[7]/td/div/ul/li/text()","//tr[9]/td/text()","//tr[6]/td/i/a/text()","//tr[10]/td/text()","//tr[8]/td/text()","//tr[6]/td/div/ul/li/text()","//tr[6]/td/i/a/text()"]


movie_count_dict = {}

for i,j,k in zip(que2_names,names_etree_data, xpath_sup):
    movie_count_dict[i] = etree_data(j, k)




ans8 = pd.DataFrame(movie_count_dict.items(), columns=['Name', 'Total Movie Appearances']).sort_values(['Total Movie Appearances'], ascending=[False])





#================================================


with open("Superhero Report.txt", 'w') as file:

    print('\nSuperhero Analysis Report\n\n', file=file)

    # As ans1a was not printing all the rows, I used ans1a.to_string() function to print all the rows.
    # I learnt it from the below link (Comment 383):
    # https://stackoverflow.com/questions/19124601/pretty-print-an-entire-pandas-series-dataframe

    print('\n1. Top 12 superheros (6+6) from both the publishers on the basis of comic appearances: \n\n', ans1a.to_string(index = False), file=file)

    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print(
        "\n\n2. The most powerful random pairs on the basis: \n\na. Six characters from each publisher with most comic appearances.\nb. Selecting first and last ranked character to form pair\n\n",
        ans1b.to_string(index=False), file=file)

    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)


    print("\n\n3. Also, the combined power of Captain America and Iron Man:\t", ans1a['Total'][7] + ans1a['Total'][9], file=file)

    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)


    print("\n\n4. Sum of earnings from top five movies of both the publishing house:\n\n", ans2a, file=file)

    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n5. Sum of earnings from all movies of both the publishing house:\n\n", ans2b, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print('\n\n6. Total number of Humans and Mutants in the final dataframe:\n\n', ans3a, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print('\n\n7. Total number of Humans and Mutants in different publishing house:\n\n', ans3b, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n8. Count of characters having particular Eye Color and Hair Color combination:\n\n", ans4, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n9. Count of Superheros based on Hair Color and Eye Color who are Living and Deceased(Dead):\n\n", ans5, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n10. Median of physical attributes of superheros on the basis of their Race:\n\n", ans6.to_string(), file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n11. Characters with most common Height(cms) amongst different publishers and race:\n\n", ans7a, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print("\n\n12. Characters with most common Weight(kgs) amongst different publishers and race:\n\n", ans7b, file=file)
    print('\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', file=file)

    print('\n\n12b. Total movie appearances of characters with most comic appearances:\n\n',
          ans8.to_string(index=False), file=file)
    print(
        '\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------',
        file=file)


#==============================

# Generating merged dataframe as csv for data visualization:

final_merged_df.to_csv("final_merged_df.csv")