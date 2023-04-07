from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import datetime
import openai

openai.api_key = ""

# issues:
# 在markets網址中，參雜了開頭為policy, business的類別
# 0407筆記，開始翻譯並寫入txt
# 0407筆記，試著用Openai翻譯後，發現限制太多，無法順利進行，故開始考慮轉換到Google translation v3

def translate_text(prompt):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.3,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  return response.choices[0].text.strip()

market_url = 'https://www.coindesk.com/markets/'
driver = webdriver.Firefox()
driver.get(market_url)

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

# 因網頁的url月與日，都是雙位數，因此變成單位數時要加上0
if len(str(month)) < 2:
    month = f'0{month}'
if len(str(day)) < 2: 
    day = f'0{day}'
year_month_day = f'{year}/{month}/{day}'

urls = []
headers = []
title = driver.find_elements(By.CLASS_NAME, "card-title")
# 在markets首頁，最下方的最新新聞，都固定只顯示六篇，故從倒數第六篇開始爬
for i in title[-6:]:
    href = i.get_attribute("href")
    if href.startswith(f'{market_url}{year_month_day}/'):
        urls.append(href)
        title = href.split(f'{year_month_day}/')[1]
        title = title.replace('-', ' ').replace('/', '')
        headers.append(title)

# for i,j in zip(headers, urls):
#     print(f"{i}\n{j}")
#     print('-'*20)
    
for i in range(len(urls)):
    resp = requests.get(urls[i-1])
    soup = BeautifulSoup(resp.text, 'html.parser')
    contents = soup.find_all('div', 'common-textstyles__StyledWrapper-sc-18pd49k-0 eSbCkN')
    paragraph=''
    for i in contents:
        paragraph = i.find('div', 'typography__StyledTypography-owin6q-0 bYmaON at-text').text
        if 'Read more:' in paragraph: 
            paragraph = paragraph.split('Read more:')[0]
            print(paragraph)
        elif 'UPDATE (' in paragraph:
            paragraph = paragraph.split('UPDATE (')[0]
            print(paragraph)
        elif 'Read the full story here:' in paragraph:
            paragraph = paragraph.split('Read the full story')[0]
            print(paragraph)
        else:
            print(paragraph)
    print('-'*30)


result = translate_text(f'translate to traditional chinese: 標題{title}\n\n內文{paragraph}')
print(result)