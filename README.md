## 「什么值得买」每日自动签到脚本


### 1. 实现功能
+ `什么值得买`每日签到
+ 通过 `钉钉群机器人` 推送通知到钉钉群
+ 通过 `SERVERCHAN` 推送简单的运行结果到微信
+ 由 `github actions` 每日早上 7 点定时运行

### 2. 使用方法
1. Fork [此仓库项目](https://github.com/flydo/smzdm_bot) > 点击右上角 fork 按钮即可，欢迎点`star`~
2. Secret新增`SMZDM_COOKIE`，填入浏览器调试模式从[什么值得买官网](https://www.smzdm.com/)cookie信息, 不懂可看下面的教程。
3. （可选）Secret新增`SERVERCHAN_SENDKEY`，获取方法请[查看文档](https://sct.ftqq.com/)。
4. （可选）钉钉群机器人通知：Secret 新增`DINGTALK_ROBOT_SECRET` 和 `DINGTALK_ROBOT_TOKEN`，获取方法请查看[「钉钉机器人」](https://developers.dingtalk.com/document/robots/custom-robot-access)。注意，需要[加签](https://developers.dingtalk.com/document/robots/customize-robot-security-settings/title-7fs-kgs-36x)。
5. fork 后必须修改一下文件，才能执行定时任务, 可修改 `README.MD`。


### 3. 其它
#### 3.1 cookie获取方法
+ 首先使用chrome浏览器，访问[什么值得买官网](https://www.smzdm.com/)， 登陆账号
+ Windows系统可按 `F12` 快捷键打开开发者工具, Mac 快捷键 `option + command + i`
+ 选择开发者工具Network，刷新页面 ,选择第一个`www.smzdm.com`, 找到`Requests Headers`里的`Cookie`。

#### 3.2 更改执行时间
在 `.github/main.yml`中
```yml
- cron: '0 0 * * *'
```
语法与 crontab 相同，具体可百度。GitHub Actions 为美区时间，＋13 小时为中国时间（即 -13 小时）。