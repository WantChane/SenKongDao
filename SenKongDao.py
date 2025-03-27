import json
import sys
import time
import datetime
import headersGenerator
import requests
import constants

import utils.path as path
from utils.logger import logger
from utils.lock import daily_lock_decorator

# 常量引入
success_code = constants.success_code
sleep_time = constants.sleep_time
sign_url = constants.sign_url
app_version = constants.app_version

# 路径引入
cookie_path = path.cookie_path

@daily_lock_decorator
def main():
    # 打印当前时间
    logger.info("当前时间为：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 读取cookie
    cookie_file = open(cookie_path, "r+", encoding="utf8")
    cookie_lines = cookie_file.readlines()
    cookie_file.close()
    logger.info(f"已读取{len(cookie_lines)}个cookie")
    logger.info(f"{sleep_time}秒后进行签到...")
    time.sleep(sleep_time)

    # 遍历cookie
    for cookie_line in cookie_lines:

        # 准备签到信息
        configs = cookie_line.split("&")
        uid = configs[0].strip()
        atoken = configs[1].strip()

        # 获取签到用的值
        cred_resp = headersGenerator.get_cred_by_token(atoken)
        sign_token = cred_resp['token']
        sign_cred = cred_resp['cred']

        # headers初始化
        init_headers = {
            'user-agent': 'Skland/'+app_version+' (com.hypergryph.skland; build:100501001; Android 25; ) Okhttp/4.11.0',
            'cred': sign_cred,
            'Accept-Encoding': 'gzip',
            'Connection': 'close',
        }

        # body
        data = {
            "uid": str(uid),
            "gameId": 1
        }

        # headers添加加密参
        headers = headersGenerator.get_sign_header(sign_url, 'post', data, init_headers, sign_token)

        # 签到请求
        sign_response = requests.post(headers=headers, url=sign_url, json=data)

        # 检验返回是否为json格式
        try:
            sign_response_json = json.loads(sign_response.text)
        except:
            logger.error(sign_response.text)
            logger.error("返回结果非json格式，请检查...")
            time.sleep(sleep_time)
            sys.exit()

        # 如果为json则解析
        code = sign_response_json.get("code")
        message = sign_response_json.get("message")
        data = sign_response_json.get("data")

        # 返回成功的话，打印详细信息
        if code == success_code:
            logger.info("签到成功")
            awards = sign_response_json.get("data").get("awards")
            for award in awards:
                logger.info(f"签到获得的奖励ID为：{award.get('resource').get('id')}")
                logger.info(f"此次签到获得了{award.get('count')}单位的{award.get('resource').get('name')}({award.get('resource').get('type')})")  # 替换为logger
                logger.info(f"奖励类型为：{award.get('type')}")
        else:
            logger.error(sign_response_json)
            logger.error("签到失败，请检查以上信息...")

        # 休眠指定时间后，继续下个账户
        time.sleep(sleep_time)

    logger.info("程序运行结束")

main()
