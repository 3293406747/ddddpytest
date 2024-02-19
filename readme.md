:link:[真希望你没见过什么世面，一生只爱我这张平凡的脸](https://music.163.com/#/song?id=1963720173)

# 带带弟弟pytest

<div>
    <a href="https://github.com/3293406747/ddddpytest/stargazers" target="_blank">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/3293406747/ddddpytest"></a>
    <a href="https://github.com/3293406747/ddddpytest/blob/main/LICENSE" target="_blank">
    <img alt="License" src="https://img.shields.io/github/license/3293406747/ddddpytest"></a>
    <a href="https://t.me/qingtest" target="_blank">
    <img alt="telegram" src="https://img.shields.io/badge/chat-telegram-blueviolet?style=flat-square&logo=Telegram"></a>
</div>

本项目实现接口自动化的技术选型：**Aiohttp+Pytest+Yaml+Excel+Smtplib** 。 其中Aiohttp用于发送和处理HTTP协议的请求接口，Pytest作为测试执行器，
YAML和Excel文件用于测试数据的管理和测试报告的生成，最后使用Smtplib发送测试报告邮件。

## 特征

- 采用协程方式发送请求，提高了测试用例执行效率
- 采用统一请求封装，session自动关联，支持多个session之间切换
- 采用关键字驱动设计，测试数据易于维护
- 自动渲染测试用例，自动处理请求中的文件，并能自动提取请求和响应中的内容进行断言
- 项目运行时自动生成日志文件和测试报告，且自动发送测试报告邮件
- Yaml文件可关联Excel文件，用于存储公共测试数据和测试数据
- Yaml及Excel文件中可使用变量和调用Python函数，方便测试用例编写
- 支持使用Python变量和文件变量，增加测试用例的灵活性
- 支持MySQL数据库连接及操作，同时支持生成Mock数据，便于测试用例的编写

:loudspeaker:项目开发环境：win11+python3.10

## 部署

1. 下载项目源码后，在根目录下找到**requirements_dev.txt**文件，然后通过 pip 工具安装项目运行依赖，执行命令：

```shell
pip3 install -r requirements_dev.txt
```

2. 在**debug/config/local.yaml**文件中配置数据库参数和邮件参数。
3. 在**debug/db**目录中找到**user.sql**并运行初始化数据库。
4. 在**debug/flask_app**目录中运行**api.py**启动服务。
5. 之后运行**main.py**，或在Terminal窗口cd到项目根目录后执行命令：

```shell
pytest
```

## 示例

```python
from common.read.case import read_case
from debug import auto_request
from debug.script.conftest import parametrize


@parametrize(read_case("debug/testcase/method.yaml"))
async def test_get(case):
	await auto_request(case)
```

```yaml
# method.yaml
- casename: get请求
  request:
    url: http://127.0.0.1:5000/get
    method: GET
    params:
      foo1: bar1
      foo2: bar2
```

## 支持

1. 如果喜欢ddddpytest，欢迎在GitHub上进行Star。
2. 本项目使用过程中遇到问题或一起交流学习欢迎添加我的微信或[Telegram](https://t.me/qingtest) 进行沟通。

![vx](system/img/vx.jpg)
