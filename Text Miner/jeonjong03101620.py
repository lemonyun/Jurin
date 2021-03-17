import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt

base_url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'

txt = ''
okt = Okt()

def keyword_extractor(tagger, text):
    tokens = tagger.phrases(text)
    tokens = [ token for token in tokens if len(token) > 1 ] # 한 글자인 단어는 제외
    count_dict = [(token, text.count(token)) for token in tokens ]
    ranked_words = sorted(count_dict, key=lambda x:x[1], reverse=True)[:10]
    return [ keyword for keyword, freq in ranked_words ]

def news_read(url):
    global txt
    req = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    #news_titles = soup.select('#wrap > div.rankingnews > div.rankingnews_box._officeResult > div > ul > li > div > a')
    news_titles = soup.select('#main_content > div > div._persist > div > div > div.cluster_body > ul > li > div.cluster_text > a')
    print(news_titles)
    # for i in news_titles:
    #     #print(i.text)
    #     txt = txt + i.text
    #     #print(i.get('href'))
    #     #print()

def clickMe():
    url = base_url+'015'
    news_read(url)
    url = base_url+'023'
    news_read(url)
    url = base_url+'277'
    news_read(url)
    url = base_url+'020'
    news_read(url)
    url = base_url+'020'
    news_read(url)
    url = base_url+'437'
    news_read(url)
    url = base_url+'052'
    news_read(url)


#clickMe()
news_read(base_url)
#print(txt)
n_list = okt.nouns(txt)
n_dict = {}
for t in n_list:
	if t in n_dict:
		n_dict[t] += 1
	else:
		n_dict[t] = 1
#print(n_dict)
for y,v in sorted(n_dict.items(),key = lambda x:x[1]):
		print(y,v)
'''
s_dict = sorted(n_dict.items(), key = lambda x:x[1])
print(type(s_dict))
for k,v in s_dict.items():
	print(v,k)
'''