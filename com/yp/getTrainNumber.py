# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import ImageFilter
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from aip import AipOcr
from PIL import Image
from aip import AipImageClassify
import re
import requests
from com.yp.TrainData import Train

APP_ID1 = '11483939'
API_KEY1 = 'M9cQBpPsWCw0SvXIxc0UW7vg'
SECRET_KEY1 = 'GejTozGHBEUP3ku3WGHbjyqGTjgTCncS'

APP_ID2 = '11480013'
API_KEY2 = 'vmarp2WH1hgdpqRoywjHDL78'
SECRET_KEY2 = 'RoTHW97LYFkjPqlQWuouXXxGQEL0QeLk'

client = AipOcr(APP_ID1, API_KEY1, SECRET_KEY1)
client2 = AipImageClassify(APP_ID2, API_KEY2, SECRET_KEY2)

# 准备一下头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_39418dcb8e053c84230016438f4ac86c=1526433568; Hm_lpvt_39418dcb8e053c84230016438f4ac86c=1526433568",
    "Host": "biz.trace.ickd.cn",
    "Referer": "http://103.46.128.47:47720/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

list = []

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)

class TrainTicketSpider(object):

    def __init__(self, depCity, arrCity, depdate):
        self.depCity = depCity
        self.arrCity = arrCity
        self.depDate = depdate
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
        # self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
        self.browser = browser

    def crawl(self):
        # self.browser.set_page_load_timeout(30)
        # self.browser.get(url)
        self.browser.switch_to(1)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "fromStationText")))
        time.sleep(1)
        self.browser.save_screenshot('1.png')
        # searchType = self.browser.find_element_by_id("fromStationText")
        # 始发地
        fromCity = self.browser.find_element_by_id("fromStationText")

        # 目的地
        toCity = self.browser.find_element_by_id("toStationText")

        # 出发时间
        jsString = "document.getElementById('train_date').removeAttribute('readonly')"
        self.browser.execute_script(jsString)
        date = self.browser.find_element_by_id("train_date")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("query_ticket")

        fromCity.click()
        time.sleep(0.5)
        fromCity.send_keys(self.depCity)
        fromCityClick = self.browser.find_element_by_id("citem_0")
        time.sleep(1)
        fromCityClick.click()

        toCity.click()
        time.sleep(0.5)
        toCity.send_keys(self.arrCity)
        toCityClick = self.browser.find_element_by_id("citem_1")
        time.sleep(1)
        toCityClick.click()

        date.click()
        date.clear()
        time.sleep(0.5)
        date.send_keys(self.depDate)

        time.sleep(0.5)
        searchBtn.click()
        WebDriverWait(self.browser, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "t-list")))
        time.sleep(2)
        # self.browser.switch_to.window(self.browser.window_handles[1])
        # self.browser.save_screenshot('3.png')


        self.parse(current_page=1, date=self.depDate)
        # except Exception as e:
        #     # print("爬取失败", e)
        #     self.browser.quit()

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        fly_list = HTML.xpath('//tbody[@id="queryLeftTable"]/tr')

        for li in fly_list:
            if li.xpath(".//td"):
                self.getData(li, date)
            else:
                continue

        print('爬取结束')
        # 关闭数据库
        self.browser.quit()

    def getData(self, li, date):
        # 车次/类型
        train = li.xpath('.//td[1]/div[1]/div[@class="train"]/div[1]/a/text()')[0]
        # print('正在获取车次型号>>>', train)

        start_station = li.xpath('.//td[1]/div[1]/div[@class="cdz"]/strong[1]/text()')[0]
        end_station = li.xpath('.//td[1]/div[1]/div[@class="cdz"]/strong[2]/text()')[0]

        # 出发时间/到达时间
        start_time = li.xpath('.//td[1]/div[1]/div[@class="cds"]/strong[@class="start-t"]/text()')[0]
        end_time = li.xpath('.//td[1]/div[1]/div[@class="cds"]/strong[@class="color999"]/text()')[0]

        # 运行时间
        duration = li.xpath('.//td[1]/div[1]/div[@class="ls"]/strong/text()')[0].strip('\n ')

        if li.xpath('.//td[2]/div/text()'):
            businessSit = li.xpath('.//td[2]/div/text()')[0]
        else:
            businessSit = li.xpath('.//td[2]/text()')[0]

        if li.xpath('.//td[3]/div/text()'):
            firstSit = li.xpath('.//td[3]/div/text()')[0]
        else:
            firstSit = li.xpath('.//td[3]/text()')[0]

        if li.xpath('.//td[4]/div/text()'):
            secondSit = li.xpath('.//td[4]/div/text()')[0]
        else:
            secondSit = li.xpath('.//td[4]/text()')[0]

        highSoft = li.xpath('.//td[5]//text()')[0]

        soft = li.xpath('.//td[6]/text()')[0]

        moveSoft = li.xpath('.//td[7]/text()')[0]

        hardSoft = li.xpath('.//td[8]/text()')[0]

        softSit = li.xpath('.//td[9]/text()')[0]

        hardSit = li.xpath('.//td[10]/text()')[0]

        noSit = li.xpath('.//td[11]/text()')[0]

        other = li.xpath('.//td[12]/text()')[0]

        if li.xpath('.//td[13]/a/text()'):
            operation = "预定"
        else:
            operation = None
        trainInfo = Train(train, start_station, end_station, start_time + "--" + end_time, duration, businessSit, firstSit, secondSit, highSoft,
                          soft, moveSoft, hardSoft, softSit, hardSit, noSit, other, operation)

        list.append(trainInfo)


        # 参考票价
        # if li.xpath('.//td[@class="no-br"]/a'):
        #     ticket_remain = "有"
        #     ticket_click = self.browser.find_elements_by_xpath('.//td[@class="no-br"]/a')[0]
        #     ticket_click.click()
        #     # print(self.browser.window_handles)
        # else:
        #     ticket_remain = "没有"
        # print('当前车次%s,[%s]票>>>' % (train, ticket_remain))


class loginUser(object):

    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
        # self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
        self.browser = browser


    def crawl(self):

        # self.browser.set_page_load_timeout(30)
        self.browser.get(self.url)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "touclick-image")))
        time.sleep(8)
        username = self.browser.find_element_by_id("username")
        password = self.browser.find_element_by_id("password")

        button = self.browser.find_element_by_id("loginSub")

        username.clear()
        username.send_keys(self.username)
        time.sleep(0.5)

        password.clear()
        password.send_keys(self.password)
        time.sleep(0.5)

        self.get_img()
        aa = self.identityUmg()
        for i in aa:
            arr = str(i).split(" ")
            for j in arr:
                if int(j) > 4:
                    y = 1
                    x = int(j) - 1 - 4
                else:
                    y = 0
                    x = int(j) - 1
                left = 5 + (67 + 5) * x
                top = 41 + (67 + 5) * y
                right = left + 67
                bottom = top + 67
                action = ActionChains(self.browser)
                action.move_to_element_with_offset(self.browser.find_element_by_class_name("touclick-image"),
                                                   left + 40,
                                                   top + 40).click().perform()
        time.sleep(1)
        button.click()
        time.sleep(4)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "my12306page")))
        self.browser.find_element_by_id("selectYuding").click()
        getTrainInfo("上海", "北京", "2018-07-20")

    def get_img(self):
        # self.browser.set_window_size(1920, 1080)
        self.browser.save_screenshot('1.png')
        img = self.browser.find_element_by_class_name("touclick-image")
        print(img.location)  # 打印元素坐标
        print(img.size)  # 打印元素大小
        left = img.location['x']
        top = img.location['y']
        right = img.location['x'] + img.size['width']
        bottom = img.location['y'] + img.size['height']
        im = Image.open('1.png')
        im = im.crop((left, top, right, bottom))
        im.save('1.png')

    def identityUmg(self):
        files = {'file': open("1.png", 'rb')}
        url = 'http://103.46.128.47:47720/'
        request23 = requests.post(url=url, headers=headers, files=files)
        # 自动解码
        # print(request23.text)
        imgre = re.compile(r'<B>(.*?)</B>')
        res = re.findall(imgre, repr(request23.text))
        print(res)
        return res

# if __name__ == '__main__':
#     url = 'https://kyfw.12306.cn/otn/leftTicket/init'
#     spider = TrainTicketSpider(depCity="上海", arrCity="北京", depdate="2018-07-20")
#     spider.crawl(url)

def getTrainInfo(depCity, arrCity, depDate):
    # url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    spider = TrainTicketSpider(depCity=depCity, arrCity=arrCity, depdate=depDate)
    spider.crawl()
    for i in list:
        print(i.trainType)
    return list

def denglu(username, password):
    url = 'https://kyfw.12306.cn/otn/login/init'
    login = loginUser(url, username, password)
    login.crawl()
    # getTrainInfo(depCity, arrCity, depDate)



