# import pandas as pd
# import numpy as np
import time, requests

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as Ureq
# from urllib.request import urlopen, Request
# import csv

def get_link_inside(container):
  take_link = container.find('a').attrs['href']
  my_url2 = str(take_link)
  uclient2 = Ureq(my_url2)
  page_html2 = uclient2.read()
  uclient2.close()
  page_soup2 = soup(page_html2,'html.parser')
  return page_soup2

def take_inf_newspaper(container):
    page_soup2 = get_link_inside(container)

    #get time
    time_bao = page_soup2.find('span',{'class': 'time'}).text.strip()
    space = time_bao[::-1].find(' ')
    time_bao = time_bao[:len(time_bao)-5]

    #get content in newspaper
    content =''
    c=0
    article_all = page_soup2.find('div',{'itemprop': 'articleBody', 'class': 'detail_content', 'id': 'detail_ct'})
    article = article_all.find_all('p')
    for x in article:
        c +=1
        if x.text == '&nbsp;':
            continue
        if c == len(article):
            continue
        content += (x.text) +'\n'
        
    #get author
    try:
        author = page_soup2.find('p', {'style': 'text-align: right;'}).text
    except:
        author = 'None'

    #get paper related (cac trang báo liên quan)
    lst_paper_related = []
    tin_lq = page_soup2.find_all('div', {'class': 'des-news'})
    # tin_lq2 = tin_lq.find_all('div', {'class': 'des-news'})
    for x in tin_lq:
        lst_paper_related.append(x.text)
    # print(lst)
    return time_bao, content, author, lst_paper_related