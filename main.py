import threading
from pygame import mixer
mixer.init()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from datetime import datetime
'''
    File name: main.py
    Author: DevHyung
    Date created: 2017-11-27
    Date last modified: 2017-11-27
    Python Version: 3.6
'''
def break_program():
    #2018 01 27 18:24
    now = 1517894603.3227959
    if time.time() > now+(60*60): #1시간뒤
        print("프로그램 만료")
        exit(-1)
    else:
        print("인증완료")
break_program()
won_perdict = {}
won_alarmdict = {}
btc_perdict = {}
btc_alarmdict = {}
doAlarm = False
delay = 5
def extractOptionFile():
    try:
        driver.get("https://upbit.com/exchange?")
        delay = 20  # seconds
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/div/div/div/div[1]/table/tbody/tr[2]/td[3]')))
        print(">>> Page is ready ! ")
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")
        with open("원화.csv", 'w') as f2:
            f2.write('코인,심볼,상승률,알람On/Off\n')
            for tr in trs:
                name = tr.find('td', class_='tit').find('a').get_text().strip()
                short = tr.find('td', class_='tit').find('em').get_text().strip()
                f2.write(name + ',' + short + ',' + '1.0,' + '1\n')
            print(">>> 원화 설정파일 다운로드 완료 ! ")
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[2]/a').click()
        time.sleep(5)
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")

        with open("BTC.csv", 'w') as f2:
            f2.write('코인,심볼,상승률,알람On/Off\n')
            for tr in trs:
                name = tr.find('td', class_='tit').find('a').get_text().strip()
                short = tr.find('td', class_='tit').find('em').get_text().strip()
                f2.write(name + ',' + short + ',' + '10.0,' + '1\n')
            print(">>> BTC 설정파일 다운로드 완료 ! ")
    except TimeoutException:
        print("ERROR : Loading took too much time!")
def openOptionFile():
    global delay
    print("_"*50)
    delay = int(input(">>> 알람 울리는 주기 입력 (초단위) :: "))
    os.system("start 원화.csv")
    input(">>> 원화 설정파일을 설정후 종료하고 엔터를 눌러주세요")
    os.system("start BTC.csv")
    input(">>> BTC 설정파일을 설정후 종료하고 엔터를 눌러주세요")
    with open("원화.csv") as f3:
        for line in f3.readlines()[1:]:
            won_perdict[line.split(',')[0]] = float(line.split(',')[2])
            won_alarmdict[line.split(',')[0]] = True if line.split(',')[-1].strip() =='1' else False
    with open("BTC.csv") as f3:
        for line in f3.readlines()[1:]:
            btc_perdict[line.split(',')[0]] = float(line.split(',')[2])
            btc_alarmdict[line.split(',')[0]] = True if line.split(',')[-1].strip() =='1' else False

def alarm():
    global doAlarm
    while True:
        if doAlarm:
            mixer.music.load('./alarm.mp3')
            mixer.music.play()
            doAlarm = False
            print("_"*50)
        time.sleep(delay)
def Observe():
    global doAlarm
    print("[Start]")
    t = threading.Thread(target=alarm)
    t.start()
    while True:
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[1]/a').click()
        time.sleep(2.5)
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")
        for tr in trs:
            name = tr.find('td', class_='tit').find('a').get_text().strip()
            percent = float(tr.find('td', class_='percent').get_text()[:-1])
            if won_perdict[name] < percent:
                if won_alarmdict[name]:
                    doAlarm = True
                    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(WON): " + name + " 감지 전일대비 "+tr.find('td', class_='percent').get_text())
                    with open('원화_log.txt', 'a') as f:
                        f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(WON): " + name + " 감지 전일대비 "+tr.find('td', class_='percent').get_text()+'\n')

        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[2]/a').click()
        time.sleep(2.5)
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")
        for tr in trs:
            name = tr.find('td', class_='tit').find('a').get_text().strip()
            percent = float(tr.find('td', class_='percent').get_text()[:-1])
            if btc_perdict[name] < percent:
                if btc_alarmdict[name]:
                    doAlarm = True
                    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(BTC): " + name + " 감지 전일대비 " + tr.find('td', class_='percent').get_text())
                    with open('BTC_log.txt', 'a') as f:
                        f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(BTC): " + name + " 감지 전일대비 "+tr.find('td', class_='percent').get_text()+'\n')
        time.sleep(5)

if __name__ == "__main__":
    dir = './chromedriver'  # 드라이브가 있는 경로
    driver = webdriver.Chrome(dir)
    driver.maximize_window()
    extractOptionFile()
    openOptionFile()
    Observe()