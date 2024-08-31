from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm , trange
import json
import time

f=open("users_url.txt","r")
listo=[]
for iln in f:
    listo.append(iln.strip())
f.close()

print('\n'*8)

with tqdm(total=len(listo)) as pbar:
    for ij in listo:
        try:
            colum = {'url':[],'name':[],'ID2':[]}
            session=HTMLSession()
            doz=session.get('https://www.mql5.com/en/users/'+ij)
            time.sleep(5)
            noma=doz.html.find("#mutualCount > span",first=True).text
            ne=ij.split('/')[-1]
            url3='https://www.mql5.com/en/users/'+ne+'/friends/mutual?limit='+str(noma)
            get3=session.get(url3)
            time.sleep(5)
            con=get3.html
            lis=con.html
            lis=json.loads(lis)
            for i in range(len(lis)):
                colum['ID2'].append(lis[i]['id'])
                colum['url'].append('https://www.mql5.com/en/users/'+lis[i]['login'])
                colum['name'].append(lis[i]['name'])
            data=pd.DataFrame(colum)
            data.to_excel(ne+'.xlsx')
            pbar.update(1)
        except:
            pbar.update(1)
            continue