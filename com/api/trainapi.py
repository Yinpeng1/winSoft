import urllib.request
import urllib.parse
import json
from com.yp.TrainData import Train

# 准备一下头
headers = {
    "Accept": "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "SESSIONID=8B9C47A2F6F52A3C98AD3F748BD69FC0; _jc_save_wfdc_flag=dc; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=4040622346.50210.0000; "
              "_jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; BIGipServerpassport=937951498.50215.0000; "
              "RAIL_EXPIRATION=1531425618092; "
              "RAIL_DEVICEID=swXNtaUp4lUqXmD70bSmm8PhXePEXkKpgaCKNeI-ZE-zU_el1ScVjGTBtRiq-6iuTaNDO1UXlocsVWpXifmfTVBBRv-9k8RvjhnhUqdwXmljGyYKPhpHp3hnkn91Bx3Qbv7axcRSGQ7h8uBEUHgnDWZezfI4iq9W; "
              "BIGipServerpool_passport=200081930.50215.0000; _jc_save_toDate=2018-07-12; ten_key=k13b7caqujAuo6z/tTBq66Tva33WabCU; "
              "ten_js_key=k13b7caqujAuo6z%2FtTBq66Tva33WabCU; current_captcha_type=Z; _jc_save_fromDate=2018-07-19",
    "Host": "kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# 还有我们准备用Post传的值，这里值用字典的形式
values = {
   'leftTicketDTO.train_date': '2018-07-19',
   'leftTicketDTO.from_station': 'SHH',
   'leftTicketDTO.to_station': 'BJP',
   'purpose_codes': 'ADULT'
}

# 将字典格式化成能用的形式
# data = urllib.parse.urlencode(values).encode('utf-8')

# 这个是百度翻译api的地址
# url = 'https://biz.trace.ickd.cn/yd/' + values.get('mailNo') + '?'+data.decode("utf-8")

list=[]

def getData():
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-07-19&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT'
    # 创建一个request,放入我们的地址、数据、头
    request23 = urllib.request.Request(url, headers=headers)
    # 访问
    html = urllib.request.urlopen(request23).read().decode('utf-8')
    html = json.loads(html)
    data = html['data']['result']
    for i in data:
        item = str(i).split("|")
        print(len(item))
        train = item[3]
        start_station = "上海"
        end_station = "北京"
        start_time = item[8]
        end_time = item[9]
        duration = item[10]
        businessSit = item[32]
        firstSit = item[31]
        secondSit = item[30]
        highSoft = item[29]
        soft = item[28]
        moveSoft = item[27]
        hardSoft = item[26]
        softSit = item[25]
        hardSit = item[24]
        noSit = item[23]
        other = item[22]
        train = Train(train, start_station, end_station, start_time + "--" + end_time, duration, businessSit, firstSit,
              secondSit, highSoft,
              soft, moveSoft, hardSoft, softSit, hardSit, noSit, other)
        list.append(train)
    return list
    # print(data)
    # print(len(data))


