#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup


movie_name = input("請輸入電影名稱關鍵字： ")


# 抓取最新10頁所有文章標題
title = []
for i in range(10):
    res = requests.get('https://www.ptt.cc/bbs/movie/search?page=%d&q=%s'%(i+1, movie_name))
    soup = BeautifulSoup(res.text)
    for entry in soup.select('.r-ent'):
        title.append(entry.select('.title')[0].text)

        
# 找出標題有'雷'且有']'且沒有'Re'之分類，刪除多於之空格
title_index = []
for i in range(len(title)):
    if '雷' in title[i] and ']' in title[i] and 'Re' not in title[i]:
        title_index.append(title[i].split(']', 1)[0].split('[', 1)[1].replace(' ',''))
   

# 統計評價
good_count = 0
ordinary_count = 0
bad_count = 0
total_count = 0
for evaluation in title_index:
    if '好' in evaluation:
        good_count += 1
    elif '爛' in evaluation or '負' in evaluation:
        bad_count += 1
    elif '普' in evaluation and '好' not in evaluation and '爛' not in evaluation and '負' not in evaluation:
        ordinary_count += 1

        
# 印出結果
total_count = good_count + ordinary_count + bad_count
if total_count == 0:
    print('查無資料')
else:
    good_percent = good_count / total_count * 100
    ordinary_percent = ordinary_count / total_count * 100
    bad_percent = bad_count / total_count * 100
    print('評價總共有 %d 篇\n好雷有 %d 篇 / 好雷率為 %.2f %%\n普雷有 %d 篇 / 普雷率為 %.2f %%\n負雷有 %d 篇 / 負雷率為 %.2f %%'%(total_count, good_count, good_percent, ordinary_count, ordinary_percent, bad_count, bad_percent))

  







