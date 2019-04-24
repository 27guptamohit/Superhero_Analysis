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



rank_xpath = "//tr/td[1]/font/text()"

Rank = (tree.xpath(rank_xpath))
Rank = Rank[0:-1]



title_xpath = "//tr/td[2]/font/a/b/text()"

Title = str(tree.xpath(title_xpath))


studio_xpath = "//tr/td[3]/font/a/text()"
Studio = tree.xpath(studio_xpath)
Studio = str(Studio[1:101])



gross_xpath = "//tr/td[4]/font/b/text()"
Gross_Income = str(tree.xpath(gross_xpath))


Gross_Income = Gross_Income.replace('$','').replace(',', '').strip()






















