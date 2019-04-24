import requests
import lxml.html
import pandas as pd
from time import sleep
import numpy as np



def get_earnings() -> lxml.etree:


    url = 'https://www.boxofficemojo.com/genres/chart/?id=superhero.htm'


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



Rank = tree.xpath("//tr/td[1]/font/text()")
#I am changing the data type of all the below elements of the list to int from xpath element data type.

Rank = list(map(int, Rank[0:-1]))





Title = tree.xpath("//tr/td[2]/font/a/b/text()")
Title = list(map(str, Title))



Studio = tree.xpath("//tr/td[3]/font/a/text()")
Studio = list(map(str, Studio[1:101]))




Gross_Income = tree.xpath("//tr/td[4]/font/b/text()")
Gross_Income = list(map(str, Gross_Income))

df = pd.DataFrame(list(zip(Rank, Title, Gross_Income, Studio)), columns=['Rank','Title', 'Gross Income','Studio'])




df['Gross Income'] = [x.strip('$') for x in df['Gross Income']]
df['Gross Income'] = [x.replace(',','') for x in df['Gross Income']]
df['Gross Income'] = df['Gross Income'].astype('int64')



print(df.head())


















