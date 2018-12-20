# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:05:59 2018

@author: Mark
"""

import requests
from bs4 import BeautifulSoup

#res = requests.get("https://www.goodreads.com/book/review_counts.json", 
#                   params={"key": "r1E4UhH6xREe17fpAqAu1g", "isbns": "9781632168146"})
#print(res.json())

xml_page = requests.get("https://www.goodreads.com/book/isbn/", params={"key": "r1E4UhH6xREe17fpAqAu1g", "isbn": "0060577363"})
#print(xml_page.content)
soup = BeautifulSoup(xml_page.text, features='lxml')
#

print(soup)

OutputFile = open('ISBN.txt', 'w', encoding='utf-8')

for child in soup.get_text():
    OutputFile.write(child)
#    OutputFile.write('\n\n')

OutputFile.close()



#des = soup.find_all('description')
#
##des = soup.select('.description')
##post = soup.select('.post')
##postdate = soup.select('.navigation')
#
#for child in des:
#    print(child, "\n\n")
##print(des[0])
#
##for child in des.children:
##    print(child, "\n\n")
    
