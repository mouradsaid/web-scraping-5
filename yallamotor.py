from requests_html import HTMLSession
import pandas as pd
import time
import random
import requests

def returnnumphone(id):
    session = HTMLSession()
    url=f'https://ksa.yallamotor.com/used_cars/show_phone_lead?id={id}'
    r = session.get(url)
    datauser=r.json()
    return datauser["data"]

try:
    f = open("config.txt", encoding='utf-8' )
    url=f.readline().split('URL :')[1].strip()      
    if '?page=' in url:
        pageInit=int(url.split('?page=')[1].split('&')[0])
        beforepage=url.split('?page=')[0]
        afterpage=url.split('?page=')[1].split('&')[1]
    else:
        try:
            beforepage=url.split('?')[0]
            afterpage=url.split('?')[1]
            pageInit=1
        except:
            beforepage=url
            afterpage=''
            pageInit=1        
    maxvr=int(f.readline().split('LAST_PAGE_NUMBER (It can be left at 0 to get to the last possible page) :')[1].strip())
    times=float(f.readline().split('TIME(s) :')[1].strip())
    f.close()
except:
    print('\n'*5,'Make sure that the .confg.txt file is written correctly')
    time.sleep(8)
    sys.exit()

colum = {'Phone':[],'Titel':[],'City':[],'Page':[]}

session = HTMLSession()

while True:
    r = session.get(f'{beforepage}?page={pageInit}&{afterpage}')
    author = r.html.xpath('//*[@id="mainContent"]/div[5]/div/div[1]/div[2]',first=True).find('.border8')
    if len(author)==0:
        break
    if maxvr!=0 and pageInit==maxvr+1:
        break
    #print(len(author))
    for ads in author:
        try:
            colum['Phone'].append(returnnumphone(ads.xpath('//div[1]/div[2]/h2/a/@href')[0].split('-')[-1]))
        except:
            colum['Phone'].append(None)
                 
        try:
            colum['Titel'].append(ads.xpath('//div[1]/div[2]/h2/a')[0].text)
        except:
            colum['Titel'].append(None)
            
        try:
            colum['City'].append(ads.xpath('//div[1]/div[2]/div[3]/div[1]')[0].text)
        except:
            colum['City'].append(None)
            
        try:
            colum['Page'].append(pageInit)
        except:
            colum['Page'].append(None)
        
    print("Page Number :",pageInit)
    pageInit+=1
    time.sleep(times)


data=pd.DataFrame(colum)
data.to_excel(str(random.randint(0,99999))+'.xlsx',sheet_name='sheet1',index=False)