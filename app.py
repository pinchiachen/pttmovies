from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 抓取使用者輸入的內容
    movie_name = event.message.text
    
    # 抓取前 10 頁所有文章標題
    title = []
    page_count = 10
    for i in range(page_count):   
        res = requests.get(f'https://www.ptt.cc/bbs/movie/search?page={i+1}&q={movie_name}')
        soup = BeautifulSoup(res.text, features='lxml')
        for entry in soup.select('.r-ent'):
            title.append(entry.select('.title')[0].text)

    # 找出標題有'雷'且有']'且沒有'Re'之分類，刪除多於之空格
    title_index = []
    for i in range(len(title)-1, -1, -1):
        if '雷' in title[i] and ']' in title[i] and 'Re' not in title[i]:
            title_index.append(title[i].split(']', 1)[0].split('[', 1)[1].replace(' ',''))

    # 計算評價
    good_count = 0
    ordinary_count = 0
    bad_count = 0
    total_count = 0
    for evaluation in title_index:
        if '好' in evaluation:
            good_count += 1
        elif '爛' in evaluation or '負' in evaluation:
            bad_count += 1
        elif '普' in evaluation and '好'  not in evaluation and '爛'  not in evaluation and '負'  not in evaluation:
            ordinary_count += 1

    # 印出結果
    total_count = good_count + ordinary_count + bad_count
    if total_count == 0:
        response = '查無資料'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '查無資料'))
    else:
        good_percent = good_count / total_count * 100
        ordinary_percent = ordinary_count / total_count * 100
        bad_percent = bad_count / total_count * 100
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f'評價總共有 {total_count} 篇\n好雷有 {good_count} 篇 / 好雷率為 {good_percent:.2f} %%\n普雷有 {ordinary_count} 篇 / 普雷率為 {ordinary_percent:.2f} %%\n負雷有 {bad_count} 篇 / 負雷率為 {bad_percent:.2f} %%'))

   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
