from bs4 import BeautifulSoup
import requests
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# 輸入網址後，可以透過openai取得翻譯，並成功寫入電腦的文字檔
# openai 為 text-davinci-003
# 正嘗試使用 GPT3.5，因此開分支檔


def configure():
    load_dotenv()
configure()
openai.api_key = os.getenv('api_key')

def translate_text(prompt):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.3,
    max_tokens=2000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  return response.choices[0].text.strip()

now = datetime.now()
year = now.year
month = now.month
day = now.day

url = 'https://www.coindesk.com/business/2023/04/05/m11-credit-resumes-crypto-lending-on-maple-finance-after-ftx-spurred-pause/'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

if resp.status_code != 200:
    print('error')
    
content_box = ''
title = soup.find('h1', 'typography__StyledTypography-owin6q-0 kVbxLR').text
contents = soup.find_all('div', 'common-textstyles__StyledWrapper-sc-18pd49k-0 eSbCkN')
for i in contents:
    content = i.find('div', 'typography__StyledTypography-owin6q-0 bYmaON at-text').text
    if 'Read more:' in content: 
        content = content.split('Read more:')[0]
    elif 'UPDATE (' in content:
        content = content.split('UPDATE (')[0]
    elif 'Read the full story here:' in content:
        content = content.split('Read the full story')[0]
    else:
        pass
    content_box += content
print(content_box)
result = translate_text(f'translate to traditional chinese: 標題{title}\n\n內文{content_box}')

path = f'/Users/jacobhuang/coindesk_news/{month}/{day}/{title}.txt'
with open(path,'a') as file:
    file.writelines(f'{url}\n\n{title}\n\n{result}')
