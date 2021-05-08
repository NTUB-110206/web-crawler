import requests
from bs4 import BeautifulSoup
import json
import numpy as np

from delete_news import delete_news
from insert_news_list import insert_news_list

if __name__ == '__main__':
    delete_news("bbc")

    url = 'https://www.bbc.com/news/topics/c734j90em14t/bitcoin'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")  # 將網頁資料以html.parser
    total_page_number = soup.select("div.lx-pagination__details.gs-u-ph.qa-pagination-details span.lx-pagination__page-number.qa-pagination-total-page-number")[0].text

    print('總頁數: '+total_page_number+' 頁\n')
    u1='https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-%7Blx-commentary-data-paged%2Fabout%2Fe0031680-9c66-4936-92b5-2ba0f88bc13c%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F'
    u2='%2Fversion%2F1.5.4%2Clx-commentary-data-paged%2Fabout%2Fe0031680-9c66-4936-92b5-2ba0f88bc13c%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F'
    u3='%2Fversion%2F1.5.4%7D?timeout=5'

    page=int(total_page_number) #總頁數要改
    for i in range(1,page):
      u1=u1+str(i)+u2
    uuu=u1+str(page)+u3
    print(uuu)
    r = requests.get(uuu)
    news_type = np.array([]) #計算news_type種類 only bbc
    news_list=[] #宣告tuple 將news存到tuple，再一起進資料庫
    print(type(news_list))
    s=json.loads(r.text) #將網頁資料以html.parser
    for j in range(len(s['payload'])):
      for i in range(len(s['payload'][j]['body']['results'])):
        news = s['payload'][j]['body']['results'][i]
        
        dateadd=str(news['dateAdded'])
        title=news['title']
        content=''
        link=''
        print(j, i, dateadd)
        print(j, i, title)
        print(j, i, news['type'])
        if 'summary' in news:
          content=news['summary']
          print(j, i, content)
        if 'synopses' in news:
          if news['synopses']['medium'] != None:
            content=news['synopses']['medium']
            print(j, i, content)
          elif news['synopses']['short'] != None:
            content=news['synopses']['short']
            print(j, i, content)
          elif news['synopses']['long'] != None:
            content=news['synopses']['long']
            print(j, i, content)
        if 'url' in news:
          link="https://www.bbc.com"+news['url']
          print(j, i, link)
        
        news_list.append((dateadd,title,content,'bbc',link)) #存進tuple
        news_type=np.append(news_type, news['type'])
    news_type=np.unique(news_type)
    print(news_type)
    # CSP、STY 正常貼文 敘述在['summary']
    # MAP 影片
    # CLIP 敘述在['synopses']['medium'] 有short medium long
    # POST 類似FB twitter貼文只有title沒有網址、內容敘述

    print(news_list)

    insert_news_list(news_list)
