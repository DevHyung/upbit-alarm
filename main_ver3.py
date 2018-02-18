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
    감지초기화 횟수 추가버전
'''
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
                f2.write(name + ',' + short + ',' + '0.0,' + '1\n')
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
                f2.write(name + ',' + short + ',' + '0.0,' + '1\n')
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
    daebi = int(input(">>> 몇초 대비 로 설정하는지 숫자를 입력 (초단위) :: "))
    pumcnt = int(input(">>> 알람을 받을 펌핑 횟수 입력해주세요 (예: 2입력하면 2번이상이면 모두) :: "))
    puminit = int(input(">>> 펌핑 초기화 시간 입력 (초단위) :: "))
    print("[Start]")
    t = threading.Thread(target=alarm)
    t.start()
    won_price = {}
    btc_price = {}
    won_pumping = {}
    btc_pumping = {}

    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[1]/a').click()
    time.sleep(2)
    bs = BeautifulSoup(driver.page_source, "lxml")
    div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
    trs = div.find_all("tr")
    for tr in trs:
        name = tr.find('td', class_='tit').find('a').get_text().strip()
        price = float(tr.find('td', class_='price').get_text().replace(',',''))
        won_price[name] = price
        won_pumping[name] = 1

    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[2]/a').click()
    time.sleep(2)
    bs = BeautifulSoup(driver.page_source, "lxml")
    div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
    trs = div.find_all("tr")
    for tr in trs:
        name = tr.find('td', class_='tit').find('a').get_text().strip()
        price = float(tr.find('td', class_='price').find('strong').get_text().replace(',', ''))
        btc_price[name] = price
        btc_pumping[name] = 1

    cycleinitidx = int(puminit/daebi)
    cycleidx = 1
    while True:
        time.sleep(daebi-2)
        if cycleidx > cycleinitidx:
            cycleidx = 1
            won_pumping = won_pumping.fromkeys(won_pumping, 1)
            btc_pumping = btc_pumping.fromkeys(btc_pumping, 1)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[1]/a').click()
        time.sleep(1)
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")
        for tr in trs:
            name = tr.find('td', class_='tit').find('a').get_text().strip()
            price = float(tr.find('td', class_='price').get_text().replace(',', ''))
            percent = float((price - won_price[name]) / won_price[name]) * 100
            won_price[name] = price
            if pow(won_perdict[name],won_pumping[name]) < percent:
                if won_alarmdict[name]:
                    if won_pumping[name] >= pumcnt:
                        print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(WON): [" + name + "] " + str(
                            won_pumping[name]) + "회 펌핑감지 기존 시간대비 " + str(percent))
                        doAlarm = True
                    won_pumping[name] += 1
                    with open('원화_log.txt', 'a') as f:
                        if won_pumping[name] >= pumcnt:
                            f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(WON): [" + name + "] " + str(
                                won_pumping[name]) + "회 펌핑감지 기존 시간대비 " + str(percent)+'\n')

        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/section[2]/article[1]/span[2]/ul/li[2]/a').click()
        time.sleep(1)
        bs = BeautifulSoup(driver.page_source, "lxml")
        div = bs.find("section", class_="ty02").find("div", class_="scrollB").find("table")
        trs = div.find_all("tr")
        for tr in trs:
            name = tr.find('td', class_='tit').find('a').get_text().strip()
            price = float(tr.find('td', class_='price').find('strong').get_text().replace(',', ''))
            percent = float((price - btc_price[name]) / btc_price[name]) * 100
            btc_price[name] = price
            if pow(btc_perdict[name],btc_pumping[name]) < percent:
                if btc_alarmdict[name]:
                    if btc_pumping[name] >= pumcnt:
                        print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(BTC): [" + name + "] " + str(
                            btc_pumping[name]) + "회 펌핑감지 기존 시간대비 " + str(percent))
                        doAlarm = True
                    with open('BTC_log.txt', 'a') as f:
                        if btc_pumping[name] >= pumcnt:
                            f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "(BTC): [" + name + "] " + str(
                                btc_pumping[name]) + "회 펌핑감지 기존 시간대비 " + str(percent) + '\n')
        cycleidx+=1


if __name__ == "__main__":
    dir = './chromedriver'  # 드라이브가 있는 경로
    driver = webdriver.Chrome(dir)
    driver.maximize_window()
    extractOptionFile()
    openOptionFile()
    Observe()