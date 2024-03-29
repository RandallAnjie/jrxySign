
**此项目本意是为北京印刷学院学子提供方便，代码方面针对性的对北印信工22暑期签到进行了优化**

~~北京印刷学院服务器目前每天晚上例行维护，签到时间请自行设定到早上七点半以后~~

~~源码懒得用git上传了，新版本直接打了个包放到release里了，以后更新只更新release~~

----

## 📃签到展示

![show](.img/show.jpg)

----

## 🔑使用方法

 - 见本人博客：[http://blog.zhuanjie.ltd/index.php/2022/07/08/jrxy_auto_sign/](http://blog.zhuanjie.ltd/index.php/2022/07/08/jrxy_auto_sign/)

----

## 更新日志
### v1.8.8(beta)
 - 适配了北印信工的签到系统
 - 调整新增了签到选项为其他需要填写信息的情况
### v1.8.9
 - 完善上一版本更新的稳定性
 - 更新了日志文档
### v1.9.0(beta)
 - ~~新增本地保存登录信息session的`wise`模块，免于签到一次登录一次（未测试）~~
### v1.9.2
 - 提高代码稳定性
 - 优化[文档](http://blog.zhuanjie.ltd/index.php/2022/07/08/jrxy_auto_sign/)
### v2.5.0
 - 完成对新教务和日期变量的适配，配置文件中的extra可填写$Data表示当前UTC日期的前一天

----

## 本项目参考
 - [ZimoLoveShuang/auto-submit](https://github.com/ZimoLoveShuang/auto-submit)
 - [CarltonHere/auto-cpdaily](https://github.com/CarltonHere/auto-cpdaily)

再次感谢大佬们提供的代码以及思路

----

## 欢迎使用今日校园自动签到系统

此项目仅适北京印刷学院信息工程学院`22暑期签到`其他签到请酌情修改代码以及[config.yam](./config.yml)文件

### 免责声明

本项目为Python学习交流的开源非营利项目，仅作为程序员之间相互学习交流之用，使用需严格遵守开源许可协议。严禁用于商业用途，禁止使用本项目进行任何盈利活动。对一切非法使用所产生的后果，我们概不负责。本项目对您如有困扰请联系我删除。

### 许可证

本项目的源代码在MPL2.0协议下发布，同时附加以下条目：
* **非商业性使用** — 不得将此项目及其衍生的项目的源代码和二进制产品用于任何商业和盈利用途
