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

### 報告後新增

- 感測移動物體，拍照回傳

- 監測溫度時，一併回傳風扇狀態

## 遇到的困難

### 初期

- 原計畫以 Homeassistant 連接溫溼度感測器，依照環境狀態，判斷是否開啟電扇等設備，提供使用者較為舒適之環境。

- 過程中發現，組內所購置之智慧插座，經過多次嘗試與查詢，仍無法連結 Homeassistant，因此轉變計畫方向，改為現行做法。

### 製作過程

- 開始攝影後無法中斷
- 斷電系統無法完全控制(硬體問題:小電扇關電後重啟無反應)

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

    ![](https://i.imgur.com/XDeSrrG.jpg)

    
- 編輯圖片

    ![](https://i.imgur.com/GZG0sjV.jpg)

- 編輯指令簡介
    
    ![](https://i.imgur.com/PDQpCOr.jpg)

- DHT22 
![](https://i.imgur.com/M25k9EV.png)
![](https://i.imgur.com/vfEPsUy.jpg)

接法 
VCC 接一號位
Data 接七號位
Ground 接六號位
- 安裝Adafruit_DHT
```linux=
# 確認更新
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-dev python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
# 現在開始安裝
sudo pip3 install Adafruit_DHT

```
- 在樹梅派安裝 Telepot
``` linux=
sudo pip install telepot
```

- 安裝opencv-python
```linux=
pip3 install opencv-python
```
- 安裝 gcc,make,USB libery
```linux=
sudo apt-get install gcc
sudo apt-get install make
sudo apt-get install libusb-1.0
```
- 下載並編碼git上的USB控制程式
```linux=
git clone git://github.com/mvp/uhubctl
cd home/pi/剛剛的那個git檔案
make
```
- telegram.py
```python=
import telepot
import Adafruit_DHT
import time
from telepot.loop import MessageLoop
import cv2
import os

DHT_SENSOR = Adafruit_DHT.DHT22
# 我們接的位置
DHT_PIN = 4

# 拍攝照片
def photo():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    cv2.imwrite('test.jpg',frame)
    cap.release()
# 拍攝影片
def record(times):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc =cv2.VideoWriter_fourcc(*'mp4v')
    fps = 40
    count=0
    out = cv2.VideoWriter('output.mp4',fourcc,fps,sz)
    while cap.isOpened():
        ret,frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame,1)
            out.write(frame)
            count+=1
        if count == times*fps:
            break
    cap.release()
    out.release()
    
# 測量溫濕度
def tem():
    global humidity
    global temperature
    humidity,temperature =  Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
# telegram bot 相關指令設定
def command(msg):
    global telegramText
    global chat_id
    global temperature
    global humidity
    chat_id = msg['chat']['id']
    telegramText = msg['text']
    print(str(chat_id))
    
    if telegramText == '/record5':
        bot.sendMessage(chat_id,'Webcam turn on')
         os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        bot.sendMessage(chat_id,'start time: {0}'.format(str(time.ctime())))
        record(int(telegramText[-1]))
        bot.sendMessage(chat_id,'end time: {0}'.format(str(time.ctime())))
        bot.sendMessage(chat_id,'Record is over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText == '/record30':
        bot.sendMessage(chat_id,'Webcam turn on')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        bot.sendMessage(chat_id,'start time: {0}'.format(str(time.ctime())))
        record(int(int(telegramText[-2])*10))
        bot.sendMessage(chat_id,'end time: {0}'.format(str(time.ctime())))
        bot.sendMessage(chat_id,'Record over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText == '/record10':
        bot.sendMessage(chat_id,'Webcam turn on')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        bot.sendMessage(chat_id,'start time: {0}'.format(str(time.ctime())))
        record(int(telegramText[-2])*10)
        bot.sendMessage(chat_id,'end time: {0}'.format(str(time.ctime())))
        bot.sendMessage(chat_id,'Record over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText =='/photo':
        photo()
        bot.sendPhoto(chat_id,photo=open('test.jpg','rb'))
    if telegramText == '/off':
        bot.sendMessage(chat_id,'Webcam  turn off.')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a off')
    if telegramText == '/start':
        bot.sendMessage(chat_id,'歡迎來到請不要亂動bot,請輸入"/"選擇指令')
    if telegramText == '/video':
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText == '/tem':
        tem()
        bot.sendMessage(chat_id,'temperature={0:0.1f}*c'.format(temperature))
        bot.sendMessage(chat_id,'{0}'.format(str(time.ctime())))
    if telegramText == '/hum':
        tem()
        bot.sendMessage(chat_id,'humidity={0:0.1f}%'.format(humidity))
        bot.sendMessage(chat_id,'{0}'.format(str(time.ctime())))
bot = telepot.Bot('You token')
bot.message_loop(command)
time.sleep(8000)
```
- fan.py
自動控制風扇(用溫度來做判斷)
```python=
import os
import Adafruit_DHT
import time
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
while True:
    humidity,temperature =  Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    if(temperature >= 40):
        os.system('sudo ./uhubctl -l 1-1 -p 2 -a on')
    if(temperature <= 35):
        os.system('sudo ./uhubctl -l 1-1 -p 2 -a off')
time.sleep(5000)
```
## 指令

**/start** - 開始使用

![](https://i.imgur.com/P4eCFFr.jpg)

![](https://i.imgur.com/1tLa3Ea.jpg)


**/photo** - 拍攝照片

![](https://i.imgur.com/SqXgXjw.jpg)

**/tem** - 感測溫度

![](https://i.imgur.com/IT9DSdZ.png)

**/hum** - 感測濕度

![](https://i.imgur.com/CUGVMqc.png)

**/record5** - 錄影5秒 

**/record10** - 錄影10秒

**/record30** - 錄影30秒

![](https://i.imgur.com/ol9mLcp.jpg)



**/video** - 查看影片

![](https://i.imgur.com/m1HjKYx.jpg)


**/off**- 關閉攝像頭

![](https://i.imgur.com/iovNke0.jpg)

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

- python thread
https://www.google.com/amp/s/blog.gtwang.org/programming/python-threading-multithreaded-programming-tutorial/amp/

- face
https://www.pcmarket.com.hk/ai%E5%B9%B3%E6%B0%91%E5%8C%96-1%E5%88%86%E9%90%98%E8%A3%BD%E4%BA%BA%E8%87%89%E8%BE%A8%E8%AD%98-%E4%B8%89-%E9%81%8B%E7%94%A8%E7%AF%87/
<hr/>
