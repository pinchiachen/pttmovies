import requests
from bs4 import BeautifulSoup
from run_time import calculate_run_time

PAGE_LIMIT = 10
BASE_URL = 'https://www.ptt.cc/bbs/movie/search'
DEFAULT_RESULT_MSG = '查無資料'

def get_target_url(page, name):
    return (
        f'{BASE_URL}?page={page}&q={name}'
        if page and name 
        else BASE_URL
    )

def crawl_article_titles(movie_name):
    titles = []

    for page in range(1, PAGE_LIMIT + 1):
        res = requests.get(get_target_url(page, movie_name))
        soup = BeautifulSoup(res.text, features='lxml')
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
    return ('好' in tag)

def is_tag_bad(tag = ''):
    return (('爛' in tag) or ('負' in tag))

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

def get_result_msg(good_count, ordinary_count, bad_count, total_count):
    msg = DEFAULT_RESULT_MSG

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
        f'評價總共有 {total_count} 篇\n好雷有 {good_count} 篇 / 好雷率為 {good_percent:.2f} %%\n'
        f'普雷有 {ordinary_count} 篇 / 普雷率為 {ordinary_percent:.2f} %%\n'
        f'負雷有 {bad_count} 篇 / 負雷率為 {bad_percent:.2f} %%'
    )

@calculate_run_time
def main():
    movie_name = input("請輸入電影名稱關鍵字： ")

    titles = crawl_article_titles(movie_name)

    title_tags = get_target_tags(titles)

    (
        good_count,
        ordinary_count,
        bad_count,
        total_count,
    ) = calculate_tags(title_tags)

    print(get_result_msg(good_count, ordinary_count, bad_count, total_count))

if __name__ == "__main__":
    main()
