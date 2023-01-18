import requests
import random
import urllib.parse
import execjs
import json



loginSession = requests.session()
loginSession.get('http://10.10.0.2/eportal/index.jsp')  # 这里会设置一个Cookies 作为会话验证


try:
    url_rediret = loginSession.get(
        "http://123.123.123.123",timeout=1)  # 这里获取到之后构建qurey的连接用来构建头文件
except requests.exceptions.ConnectTimeout:
    print("当前用户在线")
    exit(1)

mac_string = ">"+url_rediret.text.split("&mac")[1][1:33]
url_login = url_rediret.text.split("'")[1]  # 这里获得到重定向的连接 (包含之后构建头的各种信息)
get_Headers_Target = url_login
get_Headers = {  # 这里是 获取到浏览器页面的头构成 ,session自带cookies管理
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': '10.10.0.2',
    'Pragma': 'no-cache',
    'Referer': 'http://123.123.123.123/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

# 这里模拟浏览器对主页面进行一次主登录界面的获取
loginSession.get(get_Headers_Target, headers=get_Headers)


# 提取 query 相关信息用于构建之后的头文件
# 没有进行 prase 的 queryString wlanuserip=896
queryCheck_raw = url_login.split("?")[1]
queryCheck_cooked = urllib.parse.quote(
    queryCheck_raw)  # 进行urlencode后面的编码 wlanuserip%3D896




def send_pageInfo():
    # http://10.10.0.2/eportal/InterFace.do?method=pageInfo post
    pageInfo_Target = "http://10.10.0.2/eportal/InterFace.do?method=pageInfo"
    pageInfo_Header = {
        'Host': '10.10.0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'http://10.10.0.2',
        'Referer': url_login,  # 这里为唯一变量
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    pageInfo_Data = {
        'queryString':  queryCheck_raw  # 这里为唯一变量
    }
    loginSession.post(url=pageInfo_Target,
                      data=pageInfo_Target, headers=pageInfo_Header)

def send_getServices():

    # http://10.10.0.2/eportal/InterFace.do?method=getServices&queryString=wlanuserip%3D8960
    pageInfo_Target = 'http://10.10.0.2/eportal/InterFace.do?'
    getServices_Headers = {
        'Host': '10.10.0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'http://10.10.0.2',
        'Referer': url_login,  # 这里为唯一变量
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    getServices_Data = {
        'method': 'getServices',
        'queryString': queryCheck_raw
    }
    loginSession.post(url=pageInfo_Target,
                      headers=getServices_Headers, data=getServices_Data)





def get_Encrypted(passwd):
    js_code = open('/root/FuckSchoolNet/auth.js',encoding='utf-8').read()
    ctx = execjs.compile(js_code)
    return ctx.call('encryptedPassword',passwd)


def beauty_result(result,mode):
    res = json.loads(result)['result']
    mess = json.loads(result)['message']

    if mode == 'login':

        print(res)
        print(mess)
        return res
    elif mode == 'getInfo':
        print(res)
        print(mess)
        return res
    else :
        print('Error GetResunlt Bug here')


def decode_Response(target):
    """
    传入的对象应该是一个Requests 对象
    
    """
    return target.text.encode('raw_unicode_escape').decode()



def send_Login():
    # http://10.10.0.2/eportal/InterFace.do?method=login
    CurrentUser = [('19940001', 'Hash34281141')]

    login_Post_Locate = 'http://10.10.0.2/eportal/InterFace.do?method=login'
    post_Header = {
        'Host': '10.10.0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'http://10.10.0.2',
        'Referer': url_login,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    thisChoise = random.randint(0, len(CurrentUser)-1)
    post_Content = {
        'userId': CurrentUser[thisChoise][0],
        'password': get_Encrypted(CurrentUser[thisChoise][1]+mac_string),
        'queryString': queryCheck_cooked,
        'service': 'internet',
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'true'
    }

    # getResult

    r = loginSession.post(
        login_Post_Locate, data=post_Content, headers=post_Header)
    
    result = decode_Response(r)
    mess = beauty_result(result,'login')
    if mess == 'success':
        print('登入成功')
    else:
        print(mess)





def get_OnlineInfo():
    OnlineInfo_Target = 'http://10.10.0.2/eportal/InterFace.do?method=getOnlineUserInfo'

    o = loginSession.get(OnlineInfo_Target,headers=get_Headers)
    result = decode_Response(o)
    res = beauty_result(result,mode='getInfo')

    if res == 'fail':
        print('目前用户不在线,尝试登录')
        send_pageInfo()
        send_getServices()
        send_Login()
    else :
        print('当前用户在线')





get_OnlineInfo()
exit(0)
