import requests
import speech_recognition as sr
import time
from playrobot import TTS
import pygame
#使用語音辨識取得使用者輸入的城市名稱
def get_city_name():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請說出欲查詢的城市名稱：")
        pygame.mixer.init()
        pygame.mixer.music.load("city.mp3")
        pygame.mixer.music.play()
        time.sleep(2)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        city_name = recognizer.recognize_google(audio, language='zh-TW')
        print(f"你輸入的城市名稱是：{city_name}")
        TTS.wordToSound("你輸入的城市名稱是：")
        TTS.wordToSound(city_name)
        return city_name
    except sr.UnknownValueError:
        print("抱歉，無法辨識你的語音")
        pygame.mixer.init()
        pygame.mixer.music.load("sorry.mp3")
        pygame.mixer.music.play()
        return None

city_name = get_city_name()

if not city_name:
    exit()

#將 "台" 轉換成 "臺"
if city_name.startswith("台"):
    city_name = city_name.replace("台", "臺")

url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-ECE35607-AEC5-4515-BAEB-BE5CAFCE5FF1&format=JSON&locationName=&elementName='
data = requests.get(url)

#檢查 API 請求是否成功
if data.status_code != 200:
    print(f"API 請求失敗，錯誤代碼：{data.status_code}")
    exit()

data_json = data.json()
location = data_json['records']['location']

#檢查 location 是否為空
if not location:
    print(f"找不到 {city_name} 的天氣資料")
    exit()

#只顯示該城市的天氣預報結果
for i in location:
    if i['locationName'] == city_name:
        city = i['locationName']
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
        pop8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']
        print(f'{city}:\n未來8小時 {wx8}\n降雨機率 {pop8} %\n')
        TTS.wordToSound(city_name + "未來8小時" + wx8 + "降雨機率" + pop8 + "%")
        
        if "晴" in wx8:
            pygame.mixer.init()
            pygame.mixer.music.load("sun.mp3")
            pygame.mixer.music.play()
            print("今天是晴天，很適合出門走走~")
        elif "陰" in wx8:
            pygame.mixer.init()
            pygame.mixer.music.load("mix.mp3")
            pygame.mixer.music.play()
            print("天氣陰晴不定，出門要注意!")
        elif "雨" in wx8:
            pygame.mixer.init()
            pygame.mixer.music.load("rain.mp3")
            pygame.mixer.music.play()
            print("今天看起來會下雨，記得帶把傘!")
        break
