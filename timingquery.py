import requests
import logging
import time

# 获取logger对象,取名mylog
logger = logging.getLogger("mylog")
# 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
logger.setLevel(level=logging.DEBUG)

# 获取文件日志句柄并设置日志级别，第二层过滤
handler = logging.FileHandler(filename='log.txt', encoding="utf-8",mode="a")
handler.setLevel(logging.INFO)

# 生成并设置文件日志格式，其中name为上面设置的mylog
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 为logger对象添加句柄
logger.addHandler(handler)

# 记录日志
# logger.info("测试日志")

getIpUrl = 'http://members.3322.org/dyndns/getip'
sendIpUrl = 'https://sctapi.ftqq.com/SCT48642Th6ZTJIBl05JwGnOOxcbVmAwi.send?'
getIpRes = requests.get(getIpUrl)  # 获取IP
# 校验获取 ip 是否成功
if getIpRes.status_code == 200 and getIpRes.text is not None:
    # 格式化成2016-03-20 11:45:39形式
    dateTime = time.strftime("%Y-%m-%d", time.localtime())
    dateTime1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    titleText = getIpRes.text + dateTime
    despText = '发送时间：' + dateTime1 + '\n' + '发送地址：' + getIpRes.text + '备　　注：' + '自行脑补'
    sendRes = requests.get(sendIpUrl + 'title=' + titleText + '&desp=' + despText)  # 发送消息
    try:
        data = sendRes.json()
        # 校验调用 server酱 返回的信息，是否发送成功
        if sendRes.status_code == 200 and data['code'] == 0 and data['data']['error'] == 'SUCCESS':
            logger.info('>>>发送成功：' + getIpRes.text.rstrip("\n") + '<<<')
        else:
            logger.error('>>>发送失败：' + sendRes.text + '<<<')
    except:
        logger.error('>>>发送异常：' + sendRes.text + '<<<')
else:
    logger.error('>>>查询IP异常：' + getIpRes.text + '<<<')

