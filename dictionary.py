import requests
from bs4 import BeautifulSoup

word_url = 'https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{0}'
dic_url = 'https://dictionary.cambridge.org'

def get_resource(url):
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
  'AppleWebKit/537.36 (KHTML, like Gecko)'
  'Chrome/63.0.3239.132 Safari/537.36'}
  return requests.get(url, headers=headers, cookies={'over18':'1'})

def generate_search_url(url, keyword):
  url = url.format(keyword) 
  return url

# 建立soup物件 
def parse_html(r):
  if r.status_code == requests.codes.ok: 
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'lxml')
  else:
    # print('HTTP請求錯誤...') 
    soup = None
  return soup

def get_word_info(soup):
  if not soup.find('span', class_='hw dhw'):
    return None
  name = soup.find('span', class_='hw dhw').string
  s_div = soup.find_all('div', class_ = 'pr entry-body__el') 
  data = []
  for s in s_div:
    if not s.find('span', class_ = 'pos dpos'):
      pos = None
    else:
      pos = s.find('span', class_ = 'pos dpos').string
    pronounce = get_pronounce_audio(s)
    word_def = get_pos_info(s)
    data.append({
      'pos': pos,
      'pronounce': pronounce,
      'def': word_def
    })

  return {'name': name, 'data': data}

def get_pronounce_audio(soup):
  src = []
  if not soup.find_all('source', type='audio/mpeg'):
    return {'pronounce_uk': None,'pronounce_us': None}
  audio = soup.find_all('source', type='audio/mpeg')
  for a in audio:
    src.append(a.get('src'))
  return {'pronounce_uk': dic_url + src[0],'pronounce_us': dic_url + src[1]}

def get_pos_info(soup):
  word_def = []
  div = soup.find('div', class_ = 'pos-body')
  def_block = div.find_all('div', class_ = 'sense-body dsense_b')
  for d in def_block:
    def_div = d.find_all('div', class_ = 'def-block ddef_block', recursive = False)
    for d_word in def_div:
      zh_def = d_word.find(class_ = 'def-body ddef_b').span.string
      ex = get_word_ex(d_word)
      word_def.append({
        'zh_def': zh_def,
        'ex': ex
      })

  return word_def

def get_word_ex(def_block):
  example = []
  if not def_block.find_all('span',class_ = 'eg deg'):
    return None
  div = def_block.find_all('div',class_ = 'examp dexamp')
  for num in range(len(div)):
    eng_examp = zh_trans = None
    if div[num].find('span',class_ = 'eg deg'):
      eng_examp = delete_label(str(div[num].find('span',class_ = 'eg deg')))
    if div[num].find('span',class_ = 'trans dtrans dtrans-se hdb'):
      zh_trans = div[num].find('span',class_ = 'trans dtrans dtrans-se hdb').string
    example.append({
      'eng': eng_examp,
      'trans': zh_trans
    })

  return example

def delete_label(string):
  final = ''
  stack = []
  for s in string:
    if s is '<': stack.append('<')
    elif not stack : final += s
    elif s is '>': stack.pop()

  return final

def change_format(search):
  if '發音' in search:
    search = search.replace('發音','')
  if '英式' in search:
    search = search.replace('英式','')
  if '美式' in search:
    search = search.replace('美式','')
  if '例句' in search:
    search = search.replace('例句','')

  return search

def dic_scraping_bot(search):
  url = generate_search_url(word_url, change_format(search))
  soup = parse_html(get_resource(url)) 
  if soup:
    df = get_word_info(soup)

  return df
