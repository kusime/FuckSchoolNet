import requests
import json
import random
import os
import time

def decode_Response(target):
    """
    传入的对象应该是一个Requests 对象

    """
    return target.text.encode('raw_unicode_escape').decode()


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


def beauty_result(result, mode):
    res = json.loads(result)['result']
    mess = json.loads(result)['message']

    if mode == 'login':

        print(res)
        print(mess)
        return res
    elif mode == 'getInfo':
        userIndex = json.loads(result)['userIndex']
        userId = json.loads(result)['userId']
        userMac = json.loads(result)['userMac']
        print(res)
        print(mess)
        print(userId, userIndex, res, userMac)
        return (userId, userIndex, res, userMac)
    else:
        print('Error GetResunlt Bug here')


def get_Index():
    OnlineInfo_Target = 'http://10.10.0.2/eportal/InterFace.do?method=getOnlineUserInfo'

    o = requests.get(OnlineInfo_Target, headers=get_Headers)
    result = decode_Response(o)
    res = beauty_result(result, mode='getInfo')

    if res == 'fail':
        print('目前用户不在线,尝试登录')

    else:
        print('当前用户在线')
        print(res)
        return res


def cancel_SelfBind(CurrentUserInfo):
    # http://10.10.0.2/eportal/InterFace.do?method=cancelMac

    # http://10.10.0.2/eportal/InterFace.do?method=cancelMacWithUserNameAndMac

    cancel_Target = 'http://10.10.0.2/eportal/InterFace.do?method=cancelMac'

    cancel_Header = get_Headers

    cancel_Header['Referer'] = 'http://10.10.0.2/eportal/success.jsp?userIndex=' + \
        CurrentUserInfo[1]

    cancel_Data = {
        'userId': CurrentUserInfo[0],
        'usermac': ''
    }

    c = requests.post(url=cancel_Target, data=cancel_Data,
                      headers=cancel_Header)
    result = decode_Response(c)

    beauty_result(result, mode='login')


def cancel_MacBind(CurrentUserInfo):  # information turple

    # http://10.10.0.2/eportal/InterFace.do?method=cancelMacWithUserNameAndMac

    cancel_Target = 'http://10.10.0.2/eportal/InterFace.do?method=cancelMacWithUserNameAndMac'

    cancel_Header = get_Headers

    cancel_Header['Referer'] = 'http://10.10.0.2/eportal/success.jsp?userIndex=' + \
        CurrentUserInfo[1]

    cancel_Data = {
        'userId': CurrentUserInfo[0],
        'usermac': CurrentUserInfo[3].upper()
    }

    c = requests.post(url=cancel_Target, data=cancel_Data,
                      headers=cancel_Header)
    result = decode_Response(c)

    beauty_result(result, mode='login')


def offLine(CurrentUserInfo):  # information turple

    # http://10.10.0.2/eportal/InterFace.do?method=logout

    logout_Target = 'http://10.10.0.2/eportal/InterFace.do?method=logout'

    logout_Header = get_Headers

    logout_Header['Referer'] = 'http://10.10.0.2/eportal/success.jsp?userIndex=' + \
        CurrentUserInfo[1]

    logout_Data = {
        'userIndex': CurrentUserInfo[1]
    }

    l = requests.post(url=logout_Target, data=logout_Data,
                      headers=logout_Header)
    result = decode_Response(l)

    beauty_result(result, mode='login')





def getRandomMac():  # 这里获取一个随机Mac地址 随机 xx : xx 的这些
    """(RAW,COOKED),虽然说下载当前在线用户的mac用户需不要提供hhhh,同时登录的时候也可得到自动的mac注册..."""
    mac = [random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    return (':'.join(map(lambda x: "%02x" % x, mac)).upper(), "".join(map(lambda x: "%02x" % x, mac)).upper())


def system_Hook():
    """
    after Mac Change And Unregister

            shell 需要做的事情就是 , 关闭现在 eth1 重新加载新 MAc
            shell 的 逻辑就是 
            -> 关闭 ifdown if_name
            -> sleep sometime
            -> ifup if_name emm还是直接用python进行系统调用

    """

    os.system('ifdown Lan_Out')
    time.sleep(1)
    os.system('ifup Lan_Out')
    time.sleep(1)
    os.system('ifconfig eth1')
    print('Interface Have Been Restarted')


def read_2Modify(ThisTaskMac):  # 提供一个Mac地址对原来的文件进行替换
    """
    读取指定行,然后生成把新配置写入到目前的文件中,为了保险起见,我使用本地文件去替代源文件
    """
    print("准备更换地址为 >>", ThisTaskMac)

    raw_config_file = open('/root/FuckSchoolNet/network_stander', mode='r+')
    raw_config_lines = raw_config_file.readlines()
    raw_config_file.seek(0) # reset pointer
    # print(raw_config_lines)
    try:
        name_lines = 22
        mac_lines = 23
        # read file
        raw_dhcp_name = raw_config_lines[name_lines]
        raw_mac = raw_config_lines[mac_lines]

        #print(raw_dhcp_name, raw_mac)
        # insert data

        raw_dhcp_name_list = raw_dhcp_name.split("'")
        raw_dhcp_name_list[1] = ['Apple_', 'Vivo_', 'Xiaomi_',
                            'Huawei_', 'Zhongxin_', 'Sanxin_', 'Ipad_','Iqoo_'][random.randint(0,7)] + ThisTaskMac[1][:random.randint(1,11)]
   

        raw_mac_list = raw_mac.split("'")
        raw_mac_list[1] = ThisTaskMac[0]
     
        cooked_dhcp_name_string = "'".join(raw_dhcp_name_list)
        cooked_mac_string = "'".join(raw_mac_list)
        
        #print(cooked_dhcp_name_string,cooked_mac_string)
        raw_config_lines[name_lines] = cooked_dhcp_name_string
        raw_config_lines[mac_lines] = cooked_mac_string   
        
        new_config_file = open('/etc/config/network', mode='w')
        new_config_file.writelines(raw_config_lines)
        new_config_file.close()
        print('Config rewrite done')
        system_Hook()


    except IndexError:
        print('文件读取失败,可能有BUg')
        exit(1)



CurrentUserInfo=get_Index()

if CurrentUserInfo[2] == 'fail':# 还没有登录的情况 ... 不过这个一般会比较少,因为下线换mac 是主动的行为
    print('当前用户没有登录')
    print('尝试登陆后再运行这个脚本')
    exit(1)
else: #登录了就可以继续换mac然后下线的操作
    cancel_SelfBind(CurrentUserInfo)
    cancel_MacBind(CurrentUserInfo)
    offLine(CurrentUserInfo)
    ThisTaskMac = getRandomMac()
    read_2Modify(ThisTaskMac)
    time.sleep(1)
    time.sleep(2)
    import getNet #直接调用另一个脚本进行自动登录 # 不过再这个行为之前需要更换Mac 和 Ip
    exit(0)

# print(ThisTaskMac)
# repeat again


CurrentUserInfo=get_Index()

if CurrentUserInfo[2] == 'fail':# 还没有登录的情况 ... 不过这个一般会比较少,因为下线换mac 是主动的行为
    print('当前用户没有登录')
    print('尝试登陆后再运行这个脚本')
    exit(1)
else: #登录了就可以继续换mac然后下线的操作
    cancel_SelfBind(CurrentUserInfo)
    cancel_MacBind(CurrentUserInfo)
    offLine(CurrentUserInfo)
    ThisTaskMac = getRandomMac()
    read_2Modify(ThisTaskMac)
    time.sleep(1)
    time.sleep(2)
    import getNet #直接调用另一个脚本进行自动登录 # 不过再这个行为之前需要更换Mac 和 Ip
    exit(0)


