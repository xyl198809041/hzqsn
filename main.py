import pack.pyChrome as chrome

web = chrome.WebBrowser(False, False, 10)
id = ""


def login():
    global id
    rt = web.PostJson('http://183.247.236.130:8082/youngcenter_web_app/index', {
        'cardNo': '330105201603233458',
        'password': 'eWr9aj1RNGxS/XCfk7MLXQ=='
    })
    id = rt['msg']['successID']


def classList(campusid: int = 4, term: int = 0):
    classList = 'http://183.247.236.130:8082/youngcenter_web_app/appClass/classList?campusid=%d&specialtyid=&scheduleName' \
                '=&stdateTime=&enddateTime=&term=%d&sexType=1&minAge=2016/3/23&abilitys=&attitudes=&page=1&pageSize' \
                '=100 '
    rt = web.GetJson(classList % (campusid, term))
    data = [{'id': x['id'],'day':x['subject'][0:2], 'time': x['subject'][3:5], 'name': x['specialtyName']} for x in rt['msg']]
    return data


def getclass(class_id: str = '164897'):
    rt = web.PostJson('http://183.247.236.130:8082/youngcenter_web_app/appApply/enlistClass', {
        'successID': id,
        'classId': class_id,
        'type': 3
    })
    return rt['code'] == 1


login()
data=classList()
getclass(data[1]['id'])
print(1)
