import telepot
import Adafruit_DHT
import time
import datetime
from telepot.loop import MessageLoop
import cv2
import os
import numpy as np
def photo():
    cap = cv2.VideoCapture(0)
    width = 1280
    height = 960

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

    area = width * height

    ret,frame = cap.read()
    avg = cv2.blur(frame,(4,4))
    avg_float = np.float32(avg)

    while(cap.isOpened()):
        ret,frame = cap.read()
        if ret == False:
            break
        
        blur = cv2.blur(frame,(4,4))

        diff = cv2.absdiff(avg,blur)

        gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,25,255,cv2.THRESH_BINARY)

        kernel = np.ones((5,5),np.uint8)
        thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations = 2)
        thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations = 2)

        cnts,cntImg=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < 25000:
                continue
            if cv2.contourArea(c) >100000:
                break

            #cv2.imwrite('test.jpg',frame)
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite('test.jpg',frame)
            bot.sendPhoto(chat_id,photo=open('test.jpg','rb'))
        cv2.drawContours(frame,cnts,-1,(0,255,255),2)
    cap.release()
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
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
    print("finish")  
    cap.release()
    out.release()
def tem():
    global humidity
    global temperature
    humidity,temperature =  Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
def command(msg):
    global telegramText
    global chat_id
    global temperature
    global humidity
    global status
    chat_id = msg['chat']['id']
    telegramText = msg['text']
    print(str(chat_id))
    if telegramText == '/record5':
        bot.sendMessage(chat_id,'Webcam turn on')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        print(telegramText[-1])
        starttime=str(time.ctime())
        bot.sendMessage(chat_id,'start time: {0}'.format(starttime))
        record(int(telegramText[-1]))
        endtime=str(time.ctime())
        bot.sendMessage(chat_id,'end time: {0}'.format(endtime))
        bot.sendMessage(chat_id,'Record is over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText == '/record30':
        bot.sendMessage(chat_id,'Webcam turn on')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        starttime=str(time.ctime())
        bot.sendMessage(chat_id,'start time: {0}'.format(starttime))
        record(int(int(telegramText[-2])*10))
        endtime=str(time.ctime())
        bot.sendMessage(chat_id,'end time: {0}'.format(endtime))
        bot.sendMessage(chat_id,'Record over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText == '/record10':
        bot.sendMessage(chat_id,'Webcam turn on')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a on')
        starttime=str(time.ctime())
        bot.sendMessage(chat_id,'start time: {0}'.format(starttime))
        record(int(telegramText[-2])*10)
        endtime=str(time.ctime())
        bot.sendMessage(chat_id,'end time: {0}'.format(endtime))
        bot.sendMessage(chat_id,'Record over.')
        bot.sendVideo(chat_id,video=open('output.mp4','rb'))
    if telegramText =='/photo':
        os.system('sudo ./uhubctl -l 1-1 -p -5 -a on')
        bot.sendMessage(chat_id,'webcam open')
        photo()
    if telegramText == '/off':
        bot.sendMessage(chat_id,'Webcam  turn off.')
        os.system('sudo ./uhubctl -l 1-1 -p 5 -a off')
    if telegramText == '/start':
        bot.sendMessage(chat_id,'歡迎來到不要亂動bot,請輸入"/"選擇指令')
    if telegramText == '/tem':
        tem()
        bot.sendMessage(chat_id,'temperature={0:0.1f}*c'.format(temperature))
        bot.sendMessage(chat_id,'{0}'.format(str(time.ctime())))
    if telegramText == '/hum':
        tem()
        bot.sendMessage(chat_id,'humidity={0:0.1f}%'.format(humidity))
        bot.sendMessage(chat_id,'{0}'.format(str(time.ctime())))
bot = telepot.Bot('1570762143:AAFsW9AbWuEhDic8rCo53YPQ2VW3mLQsRLY')
bot.message_loop(command)
time.sleep(8000)