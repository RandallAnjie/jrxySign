import datetime
import ctypes
import inspect
import requests

week = ["一", "二", "三", "四", "五", "六", "日"]
ipadd = "50.93.205.205:9630"


# 日志
def wlog(log):
    with open('log.txt', 'a', encoding='utf-8') as fin:
        fin.write(datetime.datetime.now().strftime(
            '--------------------%Y-%m-%d %H:%M:%S-----------------\n') + log + '\n--------------------------------------------------------\n\n')


# 结束进程函数
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# 发送消息message给sender(qq号)
# http://50.93.205.205/
def message_recal(message, sender):
    url = f"http://{ipadd}/send_private_msg"
    payload = {'user_id': sender, 'message': message}
    res = requests.get(url, params=payload)
    if res.status_code == 200:
        wlog("发送\"" + message + "\"给" + str(sender) + "成功")
        print("发送\"" + message + "\"给" + str(sender) + "成功")
    else:
        wlog("发送\"" + message + "\"给" + str(sender) + "失败，状态码：+" + str(res.status_code) + " 内容：" + str(res.text))
        print("发送失败")


# 处理加好友请求
def addFriendsequest(data):
    url = f"http://{ipadd}/set_friend_add_request"
    payload = {'flag': data['flag']}
    res = requests.get(url, params=payload)
    if res.status_code == 200:
        wlog("加好友成功\n好友账号：" + str(data['user_id']) + "\n附加信息：" + data['comment'])
        print("加好友成功\n好友账号：" + str(data['user_id']) + "\n附加信息：" + data['comment'])
        return True
    else:
        wlog("加好友失败\n好友账号：" + str(data['user_id']) + "\n附加信息：" + data['comment'] + "失败，状态码：+" + str(res.status_code) + " 内容：" + str(res.text))
        print("发送失败")
        return False
