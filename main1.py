import time
import pack.pySMS as Sms
import pack.tool

import pack.pyChrome as Chrome


def get_class(campusid: str = '1', term: str = '2'):
    rt = web.PostJson('https://www.hzqsn.com/webClass/classList', data={
        'campusid': campusid,  # 西湖边1 城北4
        'term': term,  # 暑期1 秋季2
        'sexType': '1',
        'minAge': '2016/3/23',
        'page': '1',
        'pageSize': '100'
    })
    if 'msg' in rt:
        name_list = [x['specialtyName'] for x in rt['msg']]
        Sms.SendSMS('15858291872', ','.join(name_list))
        print(name_list)


web = Chrome.WebBrowser(False)
n = 0
while True:
    get_class('1')
    time.sleep(60)
    get_class('4')
    time.sleep(60)
    get_class('1', '1')
    time.sleep(60)
    get_class('4', '1')
    time.sleep(60)
    n = n + 1
    if n % 10 == 0:
        Sms.SendSMS('15858291872', pack.tool.now_datetime())
    print(n)
