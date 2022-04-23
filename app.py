import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
from bs4 import BeautifulSoup

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

BASE_URL = 'https://www.ptt.cc/bbs/movie/search'
DEAFULT_PAGE_LIMIT = 10
DEFAULT_RESPONSE = '查無資料'

def get_target_url(page, name):
    return (
        f'{BASE_URL}?page={page}&q={name}'
        if page and name
        else BASE_URL
    )

def crawl_article_titles(movie_name, max_page):
    titles = []

    for page in range(1, max_page + 1):
        res = requests.get(get_target_url(page, movie_name))
        soup = BeautifulSoup(res.text, features = 'lxml')
        for entry in soup.select('.r-ent'):
            titles.append(entry.select('.title')[0].text)

    return titles

def get_target_tags(titles = []):
    return [
        trim_title(title)
        for title in titles
        if is_title_valid(title)
    ]

def is_title_valid(title = ''):
    return (
        '雷' in title
        and '[' in title
        and ']' in title
        and 'Re' not in title
    )

def trim_title(title = ''):
    return (
        title
        .split(']', 1)[0]
        .split('[', 1)[1]
        .replace(' ', '')
    )

def is_tag_good(tag = ''):
    return '好' in tag

def is_tag_bad(tag = ''):
    return ('爛' in tag) or ('負' in tag)

def is_tag_ordinary(tag = ''):
    return (
        '普' in tag
        and '好' not in tag
        and '爛' not in tag
        and '負' not in tag
    )

def calculate_tags(tags = []):
    good_count = 0
    ordinary_count = 0
    bad_count = 0

    for tag in tags:
        if is_tag_good(tag):
            good_count += 1
        elif is_tag_bad(tag):
            bad_count += 1
        elif is_tag_ordinary(tag):
            ordinary_count += 1

    total_count = good_count + ordinary_count + bad_count

    return (good_count, ordinary_count, bad_count, total_count)

def get_response_msg(good_count, ordinary_count, bad_count, total_count):
    msg = DEFAULT_RESPONSE

    if total_count > 0:
        good_percent = (good_count / total_count) * 100
        ordinary_percent = (ordinary_count / total_count) * 100
        bad_percent = (bad_count / total_count) * 100

        msg = get_msg_content(
            total_count,
            good_count,
            good_percent,
            ordinary_count,
            ordinary_percent,
            bad_count,
            bad_percent,
        )

    return msg

def get_msg_content(
    total_count,
    good_count,
    good_percent,
    ordinary_count,
    ordinary_percent,
    bad_count,
    bad_percent,
):
    return (
        f'評價總共有 {total_count} 篇\n好雷有 {good_count} 篇 / 好雷率為 {good_percent:.2f} %\n'
        f'普雷有 {ordinary_count} 篇 / 普雷率為 {ordinary_percent:.2f} %\n'
        f'負雷有 {bad_count} 篇 / 負雷率為 {bad_percent:.2f} %'
    )

@app.route("/callback", methods = ['POST'])
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

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    movie_name = event.message.text
    print(f'movie_name: {movie_name}')

    titles = crawl_article_titles(movie_name, DEAFULT_PAGE_LIMIT)
    print(f'titles: {titles}')

    title_tags = get_target_tags(titles)
    print(f'title_tags: {title_tags}')

    (
        good_count,
        ordinary_count,
        bad_count,
        total_count,
    ) = calculate_tags(title_tags)
    print(f'good_count: {good_count}')
    print(f'ordinary_count: {ordinary_count}')
    print(f'bad_count: {bad_count}')
    print(f'total_count: {total_count}')

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = get_response_msg(
            good_count,
            ordinary_count,
            bad_count,
            total_count,
        )),
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
