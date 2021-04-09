
import requests
import time
import re
from bs4 import BeautifulSoup
import sqlalchemy

from jurinserver.app import Title, Rank
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///D:\\Jurin\\Server\\jurinserver.db')
Session = sessionmaker(bind=engine)
session = Session()
session.query(Rank).delete()
session.query(Title).delete()
session.commit()

from konlpy.tag import Okt
okt = Okt()

txt = ''


def getToday():
    return time.strftime("%m%d", time.localtime(time.time()))

today = getToday()

base_url = "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=263&sid1=101&mid=shm&date=2021"+ today

def getMaxpage():
    url = base_url + "&page=9876"
    req = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', {'class': 'paging'}).find('strong').get_text()

maxpage = int(getMaxpage())

titles = []
def makeDataset():
    latest_title = ''

    for k in range(0, maxpage):
        num = k + 1
        url = base_url + "&page=" + str(num)

        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        news_sections = soup.find('div', {'class': 'list_body newsflash_body'}).find_all('ul')

        for news_section in news_sections:
            news_titles = news_section.select('dt')
            for news_title in news_titles:

                clean_title = re.sub('[-=+,.#/\?:^$@*\"※~&ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》\r\t\n’”˚·]', '', news_title.text)
                if clean_title == '' or clean_title == '동영상기사' or clean_title == latest_title:
                    continue

                if "투자노트" in clean_title or "포토" in clean_title or "사진" in clean_title or "경제 브리핑" in clean_title:
                    continue

                latest_title = clean_title

                global txt
                txt = txt + clean_title
                print(clean_title)

                q = Title(title=clean_title)
                session = Session()
                session.add(q)
                session.commit()



makeDataset()

n_list = okt.nouns(txt)
n_dict = {}

for t in n_list:
	if t in n_dict:
		n_dict[t] += 1
	else:
		n_dict[t] = 1
l_list = []
for y,v in sorted(n_dict.items(),key = lambda x:x[1]):
    l_list.append(y)
    print(y, v)

st = ""
for i in range(-1,-11,-1):
    q = Rank(keyword=l_list[i])
    session = Session()
    session.add(q)
    session.commit()
    st = st + str(l_list[i]) + '\n'
