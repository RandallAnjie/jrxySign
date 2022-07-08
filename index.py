from tencentcloud.common.profile.http_profile import HttpProfile
from actions.wiseLoginService import wiseLoginService
from actions.autoSign import AutoSign
from actions.collection import Collection
from actions.workLog import workLog
from actions.pushKit import pushKit
from actions.Utils import Utils
from time import sleep


def start():
    Utils.log("自动化任务开始执行")
    config = Utils.getYmlConfig()
    push = pushKit(config['notifyOption'])
    httpProxy = config['httpProxy'] if 'httpProxy' in config else ''
    for user in config['users']:
        Utils.log(
            f"开始执行用户{user['user']['username'] if user['user']['username'] else '默认用户'}的任务"
        )
        if config['debug']:
            Utils.log("Debug模式")
            msg = working(user, httpProxy)
        else:
            try:
                msg = working(user, httpProxy)
                ret = True
            except Exception as e:
                msg = str(e)
                ret = False
            ntm = Utils.getTimeStr()
            if ret:
                # 此处需要注意就算提示成功也不一定是真的成功，以实际为准
                Utils.log(msg)
                if 'SUCCESS' in msg:
                    msg = push.sendMsg(
                        '今日校园签到成功通知',
                        '服务器(V%s)于%s尝试签到成功!' % (config['Version'], ntm),
                        user['user'])
                else:
                    msg = push.sendMsg(
                        '今日校园签到异常通知', '服务器(V%s)于%s尝试签到异常!\n异常信息:%s' %
                                      (config['Version'], ntm, msg), user['user'])
            else:
                Utils.log("Error:" + msg)
                msg = push.sendMsg(
                    '今日校园签到失败通知', '服务器(V%s)于%s尝试签到失败!\n错误信息:%s' %
                                  (config['Version'], ntm, msg), user['user'])
            Utils.log(msg)
    Utils.log("自动化任务执行完毕")


def working(user, httpProxy):
    wise = wiseLoginService(user['user'], httpProxy)
    # 判断wise文件是否存在
    if Utils.getWise(user['user']['username']) is None:
        Utils.log('开始尝试登录账号')
        wise.login()
        # 将wise对象保存到本地
        Utils.saveWise(wise, user['user']['username'])
    else:
        wise = Utils.getWise(user['user']['username'])
    sleep(1)
    # 登陆成功，通过type判断当前属于 信息收集、签到、查寝
    # 信息收集
    # print(user)
    try:
        if user['user']['type'] == 0:
            # 以下代码是信息收集的代码
            Utils.log('开始执行收集任务')
            collection = Collection(wise, user['user'])
            collection.queryForm()
            collection.fillForm()
            sleep(1)
            msg = collection.submitForm()
            return msg
        elif user['user']['type'] in [1, 2, 3]:
            # 以下代码是签到的代码
            Utils.log('开始执行签到任务')
            sign = AutoSign(wise, user['user'])
            sign.getUnSignTask()
            sleep(1)
            sign.getDetailTask()
            sign.fillForm()
            sleep(1)
            msg = sign.submitForm()
            return msg
        elif user['user']['type'] == 4:
            # 以下代码是工作日志的代码
            Utils.log('开始执行日志任务')
            work = workLog(wise, user['user'])
            work.checkHasLog()
            sleep(1)
            work.getFormsByWids()
            work.fillForms()
            sleep(1)
            msg = work.submitForms()
            return msg
    except Exception as e:
        if "没有未签到的任务" in str(e):
            return e
        else:
            Utils.log('开始尝试登录账号')
            wise.login()
            # 将wise对象保存到本地
            Utils.saveWise(wise, user['user']['username'])
            if user['user']['type'] == 0:
                # 以下代码是信息收集的代码
                Utils.log('开始执行收集任务')
                collection = Collection(wise, user['user'])
                collection.queryForm()
                collection.fillForm()
                sleep(1)
                msg = collection.submitForm()
                return msg
            elif user['user']['type'] in [1, 2, 3]:
                # 以下代码是签到的代码
                Utils.log('开始执行签到任务')
                sign = AutoSign(wise, user['user'])
                sign.getUnSignTask()
                sleep(1)
                sign.getDetailTask()
                sign.fillForm()
                sleep(1)
                msg = sign.submitForm()
                return msg
            elif user['user']['type'] == 4:
                # 以下代码是工作日志的代码
                Utils.log('开始执行日志任务')
                work = workLog(wise, user['user'])
                work.checkHasLog()
                sleep(1)
                work.getFormsByWids()
                work.fillForms()
                sleep(1)
                msg = work.submitForms()
                return msg


# 阿里云的入口函数
def handler(event, context):
    start()


# 腾讯云的入口函数
def main_handler(event, context):
    start()
    return 'Finished'


if __name__ == '__main__':
    start()
