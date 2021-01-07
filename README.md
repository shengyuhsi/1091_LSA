# 室友別再亂用我電腦

## Telegram Bot link:
t.me/NCNU_LSA_BOT

## 簡介

有時候人在外面，房間的電腦依然運作中，機器/電腦老舊，常有散熱不足的問題，容易發生危險，但我們不想隨時開啟散熱器，因此想到了過熱啟動散熱器的設計。此靈感來自我們一位機器經常過熱的室友。

而有時我們不在位子上，室友可能心癢癢地想偷看自己電腦，因此加入了攝像頭監控現場的功能。



## 設備

| 名稱 | 數量 | 來源 |
| -------- | -------- | -------- |
| 樹莓派     | 1     | 課程提供     |
| 溫溼度感測器| 1 | MOLi |
| 網路攝影機 | 1 | 自備 |
| 散熱器 | 1 | 自備 |


## 功能

- 監測感測器所屬環境
    
    - 溫度
    - 濕度
    - 現場照片
    - 現場錄影
         - 5、10、30 秒

- 溫度過高時，自動啟動散熱器散熱

- Telegram Bot 供使用者查詢

## 遇到的困難

### 初期

- 原計畫以 Homeassistant 連接溫溼度感測器，依照環境狀態，判斷是否開啟電扇等設備，提供使用者較為舒適之環境。

- 過程中發現，組內所購置之智慧插座，經過多次嘗試與查詢，仍無法連結 Homeassistant，因此轉變計畫方向，改為現行做法。

### 製作過程

- 開始攝影後無法中斷
- 斷電系統無法完全控制

## 解決方法

- Homeassistant 問題 → 更改主題
- 攝影中斷 問題 → 設定拍攝秒數
- 斷電系統無法完全控制 → 更改器材(風扇改為散熱器)

## Telegram Bot 創建

- 下載 Telegram 手機/電腦版
- 向 Bot Father 申請建立新的 Bot

    ![](https://i.imgur.com/duONFMB.png)
    
- 編輯選項

    ![](https://i.imgur.com/OCqJBmS.jpg)

- 編輯名稱

    ![](https://i.imgur.com/cJAnG2N.jpg)


- 編輯指令簡介
    
    ![](https://i.imgur.com/PDQpCOr.jpg)

- 在樹梅派安裝 Telepot
``` linux=
sudo apt-get install python-pip
sudo pip install telepot
```

## 指令

**/photo** - 拍攝照片



**/tem** - 感測溫度

![](https://i.imgur.com/IT9DSdZ.png)

**/hum** - 感測濕度

![](https://i.imgur.com/CUGVMqc.png)

**/record5** - 錄影5秒 

**/record10** - 錄影10秒

**/record30** - 錄影30秒

**/video** - 查看影片

**/off**- 關閉攝像頭

## 參考資料

- Python 
https://installvirtual.com/how-to-install-python-3-8-on-raspberry-pi-raspbian/

- Telegram Bot 
https://ithelp.ithome.com.tw/articles/10244411
https://z3388638.medium.com/telegram-bot-1-懶得自己做的事就交給機器人吧-c59004dc6c7bh
https://zaoldyeck.medium.com/%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E6%80%8E%E9%BA%BC%E6%89%93%E9%80%A0-telegram-bot-a7b539c3402a

- 監測器控制
https://ithelp.ithome.com.tw/articles/10245619
https://ithelp.ithome.com.tw/m/articles/10238029
https://tutorial.cytron.io/2019/03/14/home-notification-using-telegram-raspberry-pi/

- 攝像頭錄影
https://www.itread01.com/content/1547376124.html
https://www.instructables.com/How-to-Make-Raspberry-Pi-Webcam-Server-and-Stream-/

- Webcam 即時串流
https://www.instructables.com/How-to-Make-Raspberry-Pi-Webcam-Server-and-Stream-/
