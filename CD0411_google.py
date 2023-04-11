from bs4 import BeautifulSoup
import requests
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import translate

result =''
def translate_text(text="", project_id="able-hull-381502"):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "zh-TW",
        }
    )
    for translation in response.translations:
        result = "Translated text: {}".format(translation.translated_text)
    return result

now = datetime.now()
year = now.year
month = now.month
day = now.day

url = 'https://www.coindesk.com/consensus-magazine/2023/04/07/thanks-sam-how-ftx-led-to-worlds-worst-crypto-policy/'
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
# print(content_box)
translate_text(text = f'{title}\n\n{content_box}')
print(result)
path = f'/Users/jacobhuang/coindesk_news/{month}/{day}/{title}.txt'
with open(path,'a') as file:
    file.writelines(f'{url}\n\n{title}\n\n{result}')
 