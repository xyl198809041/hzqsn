import re
import time
import pack.pySMS as Sms
import pack.tool

import pack.pyChrome as Chrome

no_class_list = ['蹦床', '宝宝英语']


def bao_ming(class_id: str = '163310'):
    rt = web.PostJson('https://www.hzqsn.com/index?', {
        'cardNo': '330105201603233458',
        'password': 'eWr9aj1RNGxS/XCfk7MLXQ=='
    })
    success_id = rt['msg']['successID']
    rt = web.PostJson('https://www.hzqsn.com/applyweb/enlistClass', {
        'successID': success_id,
        'classId': class_id,
        'type': 1
    })
    print(rt['code'])
    return rt['code']


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
        class_list = [{
            'class_id': x['id'],
            'name': x['specialtyName'],
            'time': str2time(x['subject']),
            'point': time2point(str2time(x['subject']), x['specialtyName'])
        } for x in rt['msg']]
        best_class = max(class_list, key=lambda x: x['point'])
        if best_class['point'] > 0:
            code = bao_ming(best_class['class_id'])
            no_class_list.append(best_class['name'])
            Sms.SendSMS('13067764287', str(best_class['name']) + '尝试报名,结果为:' + str(code))
        name_list = [x['specialtyName'] for x in rt['msg']]
        Sms.SendSMS('13067764287', '地点：'+campusid+'\n'+','.join(name_list))
        print(name_list)


def str2time(s: str):
    m = re.match(r'周(\w) (\d{2}):(\d{2})-(\d{2}):(\d{2})', s)
    return {
        'start_time': int(m.group(2) + m.group(3)),
        'end_time': int(m.group(4) + m.group(5)),
        'week': m.group(1)
    }


def time2point(class_time: dict, class_name: str):
    time2point_list = {
        800: 2,
        900: 3,
        1000: 4,
        1100: 4,
        1200: 2,
        1300: 0,
        1400: 0,
        1500: 0,
        1600: 4,
        1700: 3,
        1800: 3,
        1900: 2,
        2000: 0
    }
    week2point = {
        '一': 0,
        '二': 0,
        '三': 0,
        '四': 0,
        '五': 0,
        '六': 1,
        '日': 2
    }
    time_point = 0
    week_point = 0
    if class_name in no_class_list:
        return 0
    for t in time2point_list:
        if class_time['start_time'] < t:
            time_point = time2point_list[t]
            break
    for w in week2point:
        if w == class_time['week']:
            week_point = week2point[w]
    return time_point * week_point


web = Chrome.WebBrowser(False)
n = 0
while True:
    get_class('4')
    time.sleep(60)
    n = n + 1
    if n % 10 == 0:
        Sms.SendSMS('15858291872', pack.tool.now_datetime())
    print(n)


