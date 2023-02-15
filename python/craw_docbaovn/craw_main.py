import pandas as pd
import numpy as np
import time, requests
import unidecode # xoa dau tieng viet
# import re

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as Ureq
# from urllib.request import urlopen, Request
from pymongo import MongoClient
from take_inf import get_link_inside, take_inf_newspaper
# import csv

def remove_accent(text):
    return unidecode.unidecode(text)

def connect_mongo(name_collection): #name_collection is string
    user = 'root'
    password = 'toan123' # CHANGE THIS TO THE PASSWORD YOU NOTED IN THE EARLIER EXCERCISE - 2
    host='localhost'
    #create the connection url
    connecturl = "mongodb://{}:{}@{}:27017/?authSource=admin".format(user,password,host)


    # connect to mongodb server
    print("Connecting to mongodb server")
    connection_m = MongoClient(connecturl)

    #Create database (get_database: nếu database tồn tại thì nó sẽ connect, nếu chưa sẽ tạo)
    db = connection_m.get_database('newspaper') #connection_m['newspaper']

    #Create collection in database (collection: nếu collection tồn tại thì nó sẽ connect, nếu chưa sẽ tạo)
    collection = db.get_collection(name_collection)#db[name_collection]

    return connection_m, collection

if __name__ == '__main__':
    count = 1
    check_connection=False


    for i in range(1,101):
        page_web =str(i)
        #Connect to web newspaper:
        my_url = 'https://docbao.vn/gioi-tre/p'+page_web
        uclient = Ureq(my_url)
        print("\nCheck connect: ", uclient)
        print("\nRead page:\n")
        page_html = uclient.read()
        print('=> Check Read Page {} OK'.format(page_web))
        uclient.close()
        print("\n***Close Connect***\n")

        #html parsing (phan tich cu phap)
        page_soup = soup(page_html,'html.parser')
        Topic = remove_accent(page_soup.h1.text.strip().replace('\n','').replace(' ','_').replace('-','_'))#re.sub('\W+','', remove_accent(page_soup.h1.text.replace('\n',''))) # the gioi, ..
        if Topic == "Sao_360deg":
            Topic = Topic[:len(Topic)-3]
        # print(Topic)

        # Connect to collection database (newspaper) mongodb
        if check_connection==False: # để chỉ cho connect 1 lần trong vòng lặp vì ở đây Topic ta tạo collection
            connection_m, collection = connect_mongo(Topic)
            check_connection == True

        #Link to information in page
        containers1_1 = page_soup.find('div', {'class':'category_news_list'})
        containers1_2 = containers1_1.find('ul')
        containers1 = containers1_2.find_all('li')
        print("Information newspaper in one page: ", len(containers1))

    
        # Take infor newspaper
        for container in containers1:
            count+=1
            #get title
            title = container.find('h3').find('a').text
            try: # check page and name title error
                #get Date Time, Content, author
                time_bao, content, author, paper_related = take_inf_newspaper(container)
            except:
                print('*'*30 + 'CHÚ Ý')
                print('title: ',title)
                print(page_web)
                pass
            # Split time_bao to Date and Time
            Date = time_bao.split()[0]
            Time = time_bao.split()[1]

            #Abstract paper
            abstract = container.find('p').text

            if author !='None':
                doc = {\
                        "Title": title,\
                        "Date_sub": Date,\
                        "Time_sub": Time,\
                        "Content" : content,\
                        "Abstract": abstract,\
                        "Author": author,\
                        "Paper_related": paper_related
                    }
            else:
                doc = {\
                        "Title": title,\
                        "Date_sub": Date,\
                        "Time_sub": Time,\
                        "Content" : content,\
                        "Abstract": abstract,\
                        "Paper_related": paper_related
                    }
            collection.insert_one(doc)
    # close the server connecton
    print("Closing the connection.")
    connection_m.close()



