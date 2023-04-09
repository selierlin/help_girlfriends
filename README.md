# help_girlfriends


help_girlfriends 是一款基于微信公众号和推送通知的应用，旨在帮助女朋友解决丢三落四的问题。通过定时提醒女朋友，帮助她养成良好的生活习惯。

下面是该项目的流程图：

![](./assets/流程图.png)

具体说明如下：

1. 用户在微信公众号中发送提醒指令。

2. 微信公众号通过 Werobot 框架接收到用户发送的提醒指令。

3. Werobot 解析指令，并将其转换为 Apscheduler 定时任务。

4. Apscheduler 将定时任务保存到 SQLite 数据库中。

5. Apscheduler 返回添加任务成功提示。

6. Werobot 将添加任务成功提示返回给微信公众号。

7. 微信公众号将添加任务成功提示返回给用户。



定时任务流程图：

![](./assets/定时任务.png)

## 快速开始

下面提供两种方案，一种是直接我用搭建好的，无需任何条件就可以完成；另外一个需要自备公众号、服务器

### 1. 直接使用

1. 在微信中搜索并关注 葫芦同学 公众号。
2. 将女朋友的push deer添加到已注册的用户列表中。
3. 在设置页面中，选择提醒时间和频率。
4. 等待每天的定时提醒，帮助女朋友养成好习惯。

### 2. 自行搭建

### 准备条件

1. 个人公众号，[申请地址](https://mp.weixin.qq.com/cgi-bin/registermidpage?action=index&lang=zh_CN&token=) ，创建一个**订阅号**即可。
1. Linux服务器

### 部署

#### 克隆项目

```shell
git clone https://github.com/selierlin/help_girlfriends
```

#### 配置说明

核心配置文件为 `config.json`，在项目中提供了模板文件 `config-template.json` ，可以从模板复制生成最终生效的 `config.json` 文件：

```shell
cp config-template.json config.json
```

说明

```json
{
  "db_path": "./jobs.db", # 数据库文件位置，启动的时候会生成到该位置
  "port": 5000, # 启动端口
  "we_token": "your wechat token", # 微信公众号配置的token
  "APP_ID": "your wechat appid", # 微信公众号的appid
  "APP_SECRET": "your wechat app_secret", # 微信公众号的app_secret
  "debug": false # 调试模式，默认即可
}
```

#### 安装依赖

```shell
pip install -r requirements.txt
```

#### 启动

```shell
python app.py
```

启动完后，浏览器打开链接：http://你的服务器IP/robot/ 。 当看到werobot页面说明启动成功

#### 配置公众号

##### 配置IP白名单及服务器URL

![image-20230409141320513](assets/image-20230409141320513.png)



> 配置IP白名单为你的服务器IP
>
> 配置服务器地址为：http://你的服务器IP/robot/



配置完成，使用你的公众号，回复“帮助”，收到公众号回复的消息，即可完成

## 开发和贡献

我们欢迎开发者为该项目做出贡献。如果您有任何建议或发现了任何问题，请在GitHub上提交issue或pull request。
