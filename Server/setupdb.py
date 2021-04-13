
import requests
import time
import re
from bs4 import BeautifulSoup
import sqlalchemy
from datetime import datetime, timedelta

from jurinserver.app import Title, TodayRank, WeekRank
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///D:\\Jurin\\Server\\jurinserver.db')
Session = sessionmaker(bind=engine)

session = Session()
session.query(TodayRank).delete()
session.query(WeekRank).delete()
session.commit()

## db 데이터 전체 초기화
session = Session()
session.query(Title).delete()
session.commit()

session = Session()
## weektrend test code
# for i in range(1, 100):
#     q = Title(title="코로나", date=datetime.now() + timedelta(days=-2))
#     session = Session()
#     session.add(q)
#     session.commit()

from konlpy.tag import Okt
okt = Okt()

txt = ''


today = time.strftime("%y-%m-%d", time.localtime(time.time()))
session = Session()
session.query(Title).filter(Title.date.like('%'+today+'%')).delete(synchronize_session=False)  ### db에서 오늘 읽었던 타이틀만 삭제. 아래 코드에서 db에 다시 저장할 예정
session.commit()

base_url = "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=263&sid1=101&mid=shm&date=2021"+ time.strftime("%m%d", time.localtime(time.time()))

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

makeDataset() # 당일 기사 읽어오기

def TitleToKeyword(text):
    n_list = okt.nouns(text)
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


    return l_list

todaykeywords = TitleToKeyword(txt)

st = ""
for i in range(-1,-11,-1):
    q = TodayRank(keyword=todaykeywords[i])
    session = Session()
    session.add(q)
    session.commit()
    st = st + str(todaykeywords[i]) + '\n'

txt = ""
st = ""

session = Session()
week_title_list = session.query(Title).filter(Title.date.between(datetime.now() + timedelta(days=-6), datetime.now())).all()
session.commit()



for title in week_title_list:
    txt = txt + title.title

weekkeywords = TitleToKeyword(txt)

for i in range(-1, -11, -1):
    q = WeekRank(keyword=weekkeywords[i])
    session = Session()
    session.add(q)
    session.commit()
    st = st + str(weekkeywords[i]) + '\n'



