import requests
import apprise


# 消息通知聚合类
class pushKit:
    # 初始化类
    def __init__(self, option):
        self.option = option
        self.type = option['method']

    def sendMsg(self, title, msg, user=''):
        if 'notifyOption' not in user:
            return '该用户未配置推送,已取消发送！'
        if 'rcvOption' not in user['notifyOption']:
            return '该用户未配置推送,已取消发送！'
        if user['notifyOption']['rcvOption'] == "":
            return '该用户未配置推送,已取消发送！'

        userOption = user['notifyOption']
        # 获取接收账号
        rcvOption = userOption['rcvOption']
        # 获取全局推送模式
        method = self.type
        # 获取用户指定的推送模式
        if 'method' in userOption:
            method = userOption['method']

        # 判断推送类型
        if method == 0:
            return '消息推送服务未启用'
        if method == 1:
            return self.sendMsgByMailApi(rcvOption, title, msg)
        if method == 2:
            return self.sendMsgByOther(rcvOption, title, msg)
        if method == 3:
            return self.sendMsgByQyWx(rcvOption, title, msg)
        if method == 4:
            return self.sendMsgByQQ(rcvOption, title, msg)

        return '推送参数配置错误,已取消发送！'

    # 发送邮件消息
    def sendMsgByMailApi(self, mail, title, msg):
        if mail == '':
            return '邮箱为空,已取消邮箱API发送！'
        if self.option['mailApiUrl'] == '':
            return '邮件API为空,设置邮件API后才能发送邮件'
        # 以下部分需要根据不同接口自行修改
        params = {'recipient': mail, 'title': title, 'content': msg}
        res = requests.post(url=self.option['mailApiUrl'],
                            params=params).json()
        return "邮箱API%s" % (res['message'])

    def sendMsgByOther(self, rcvOption, title, msg):
        pusher = apprise.Apprise()
        pusher.add(rcvOption)
        res = pusher.notify(
            body=msg,
            title=title,
        )

        if res == True:
            return "APPRISE推送消息成功"
        else:
            return "APPRISE推送消息失败"

    # 企业微信应用推送
    def sendMsgByQyWx(self, rcvAcc, title, message):
        wxConfig = {}

        def get_access_token(wxConfig):
            get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
            response = requests.get(get_token_url, params=wxConfig).json()
            if response.get('access_token'):
                return response['access_token']
            else:
                print(response)
                return '获取access_token失败,已取消企业微信推送'

        wxConfig['corpid'] = 'ww8cd0b3d1da2dd7c6'
        wxConfig['corpsecret'] = '8wmYYo7qB8HnURD7lp6Q1vOm-vBXIgtU95O_IbYP-tI'
        wxConfig['agentid'] = '1000006'
        if wxConfig['corpid'] and wxConfig['corpsecret']:
            try:
                access_token = get_access_token(wxConfig)
                if isinstance(access_token, str):
                    params = {
                        'touser': rcvAcc,
                        "agentid": wxConfig['agentid'],
                        "msgtype": "text",
                        'text': {
                            'content': f'{title}\n{message}'
                        }
                    }
                    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
                    response = requests.post(url=url, json=params).json()
                    # print(response)
                    return '企业微信推送成功' if response['errmsg'] == 'ok' else response
                else:
                    print(access_token)
                    return access_token
            except Exception as e:
                return '企业微信推送失败,%s' % e
        else:
            return '企业微信应用配置错误,请检查qywxOption'

    def sendMsgByQQ(self, rcvAcc, title, message):
        url = self.option['qqUrl']
        msg = title + "\n" + message + "\n" + "历史日志：http://startpage.zhuanjie.ltd/api/signlog.php"
        url = url + f"?user_id={rcvAcc}&message={msg}"
        try:
            response = requests.request("GET", url, headers={}, data={}).json()
            # print(response)
            return 'qq推送成功' if response['status'] == 'ok' else response
        except Exception as e:
            return 'qq推送失败,%s' % e
