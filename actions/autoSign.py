import json
from actions.Utils import Utils
from actions.wiseLoginService import wiseLoginService


class AutoSign:
    # 初始化签到类
    def __init__(self, wiseLoginService, userInfo):
        self.session = wiseLoginService.session
        self.host = wiseLoginService.campus_host
        self.userInfo = userInfo
        self.taskInfo = None
        self.task = None
        self.form = {}
        self.fileName = None
        self.apis = Utils.getApis(userInfo['type'])

    # 获取未签到的任务
    def getUnSignTask(self):
        headers = self.session.headers
        headers['Content-Type'] = 'application/json'
        if self.host == '':
            raise Exception('学校域名为空')
        # 第一次请求接口获取cookies（MOD_AUTH_CAS）
        url = self.host + self.apis[0]
        if url[0] != 'h':
            url = 'https://' + url
        # # 从文件读取session
        # if Utils.getSession(self.userInfo['username']) is None:
        #     # 第一次获取
        #     Utils.log('第一次获取session')
        #     self.session.post(url,
        #                       headers=headers,
        #                       data=json.dumps({}),
        #                       verify=False)
        #     # 保存session到文件
        #     Utils.saveSession(self.session, self.userInfo['username'])
        #     Utils.log('重新获取cookies成功')
        # else:
        #     Utils.log('从文件读取session')
        #     self.session = Utils.getSession((self.userInfo['username']))
        # try:
        #     # 第二次请求接口，真正的拿到具体任务
        #     res = self.session.post(url,
        #                             headers=headers,
        #                             data=json.dumps({}),
        #                             verify=False).json()
        # except Exception as e:
        #     Utils.log('获取任务失败，重新获取session')
        #     self.session.post(url,
        #                       headers=headers,
        #                       data=json.dumps({}),
        #                       verify=False)
        #     # 保存session到文件
        #     Utils.saveSession(self.session, self.userInfo['username'])
        #     Utils.log('重新获取cookies成功')
        #     # 第二次请求接口，真正的拿到具体任务
        #     res = self.session.post(url,
        #                             headers=headers,
        #                             data=json.dumps({}),
        #                             verify=False).json()
        self.session.post(url,
                          headers=headers,
                          data=json.dumps({}),
                          verify=False)
        # 第二次请求接口，真正的拿到具体任务
        res = self.session.post(url,
                                headers=headers,
                                data=json.dumps({}),
                                verify=False).json()
        if len(res['datas']['unSignedTasks']) < 1:
            if len(res['datas']['leaveTasks']) < 1:
                raise Exception('当前暂时没有未签到的任务哦！')
            latestTask = res['datas']['leaveTasks'][0]
        else:
            latestTask = res['datas']['unSignedTasks'][0]
        self.taskInfo = {
            'signInstanceWid': latestTask['signInstanceWid'],
            'signWid': latestTask['signWid']
        }

    # 获取具体的签到任务详情
    def getDetailTask(self):
        url = self.host + self.apis[1]
        headers = self.session.headers
        headers['Content-Type'] = 'application/json'
        res = self.session.post(url,
                                headers=headers,
                                data=json.dumps(self.taskInfo),
                                verify=False).json()
        self.task = res['datas']

    # 填充表单
    def fillForm(self):
        # 判断签到是否需要照片
        if self.task['isPhoto'] == 1:
            Utils.uploadPicture(self, self.apis[3], self.userInfo['photo'])
            self.form['signPhotoUrl'] = Utils.getPictureUrl(self, self.apis[4])
        else:
            self.form['signPhotoUrl'] = ''
        if 'isNeedExtra' in self.task:
            self.form['isNeedExtra'] = self.task['isNeedExtra']
        else:
            self.task['isNeedExtra'] = 0
        if self.task['isNeedExtra'] == 1:
            extraFields = self.task['extraField']
            userItems = self.userInfo['forms']
            extraFieldItemValues = []
            # print(extraFields)
            for i in range(len(extraFields)):
                userItem = userItems[i]['form']
                extraField = extraFields[i]
                if self.userInfo['checkTitle'] == 1:
                    if userItem['title'] != extraField['title']:
                        raise Exception(
                            f'\r\n第{i + 1}个配置出错了\r\n您的标题为：[{userItem["title"]}]\r\n系统的标题为：[{extraField["title"]}]'
                        )
                extraFieldItems = extraField['extraFieldItems']
                flag = False
                data = 'NULL'
                for extraFieldItem in extraFieldItems:
                    if extraFieldItem['isSelected']:
                        data = extraFieldItem['content']
                    if extraFieldItem['content'] == userItem['value']:
                        if extraFieldItem['isOtherItems'] == 1:
                            if 'value' in userItem:
                                flag = True
                                if 'extra' in userItem:
                                    inner = userItem['extra']
                                else:
                                    inner = userItem['value']
                                extraFieldItemValue = {
                                    'extraFieldItemValue': inner,
                                    'extraFieldItemWid': extraFieldItem['wid']
                                }
                                extraFieldItemValues.append(
                                    extraFieldItemValue)
                            else:
                                raise Exception(
                                    f'\r\n第{ i + 1 }个配置出错了\r\n表单未找到你设置的值：[{userItem["value"]}],\r\n该选项需要extra字段'
                                )
                        else:
                            flag = True
                            extraFieldItemValue = {
                                'extraFieldItemValue': userItem['value'],
                                'extraFieldItemWid': extraFieldItem['wid']
                            }
                            extraFieldItemValues.append(extraFieldItemValue)
                if not flag:
                    raise Exception(
                        f'\r\n第{ i + 1 }个配置出错了\r\n表单未找到你设置的值：[{userItem["value"]}],\r\n你上次系统选的值为：[{data}]'
                    )
            self.form['extraFieldItems'] = extraFieldItemValues
        self.form['signInstanceWid'] = self.task['signInstanceWid']
        self.form['longitude'] = self.userInfo['lon']
        self.form['latitude'] = self.userInfo['lat']
        self.form['isMalposition'] = self.task['isMalposition']
        self.form['abnormalReason'] = self.userInfo[
            'abnormalReason'] if 'abnormalReason' in self.userInfo else ''
        self.form['position'] = self.userInfo['address']
        self.form['uaIsCpadaily'] = True
        self.form['signVersion'] = '1.0.0'

    # 提交签到信息
    def submitForm(self):
        # print(json.dumps(self.form))
        self.submitData = self.form
        self.submitApi = self.apis[2]
        res = Utils.submitFormData(self).json()
        return res['message']
