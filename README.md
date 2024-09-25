# LineBot PTT Movies

> *因為 Heroku 沒有免費方案了，所以用 Node.js 重新寫了一個 V2 版本，並且部屬在 Vercel 上。*
> *V2 版本連結：https://github.com/pinchiachen/ptt-movie-bot*

## Description
本程式用途為輸入電影名稱關鍵字後，利用該關鍵字在 PTT_Movie 網頁板進行搜尋，抓取最新 10 頁資料，分別統計好雷、普雷及負雷數目進行分析，得知該電影在  PTT_Movie 板之評價。

## Built With
- Python
- Beautiful Soup
- Heroku

## How to use
- LINE 好友搜尋 ID：@vsr0046b，名稱為「鄉民怎麼看」，加入好友即可使用。
<br>或是透過以下 QR Code：<br>
<a href="https://imgur.com/4PXFkbz"><img src="https://i.imgur.com/4PXFkbz.png" title="source: imgur.com" /></a>

## Demo
<a href="https://imgur.com/DCWwXgR"><img src="https://i.imgur.com/DCWwXgR.png" title="source: imgur.com" /></a>

## Note
- 本程式部屬在 Heroku，要在本地端運行可以直接執行 ptt_movies.py。
- 普好雷算入好雷，普負雷算入負雷。
- app.py 為部屬在 Heroku 上執行主程式之 py 檔。
- 將執行過程中需要安裝之模組加入 requirements.txt。
- run_time.py 用來記錄爬蟲時間，以 decorator 的方式使用。

## Contact me
- chenargar@gmail.com
