# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

from spider_server.conf.config_util import ConfigUtil
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


class EmailSMTP(object):
    def __init__(self):
        self.msg_from = ConfigUtil().get("EMAIL", "msg_from")
        self.msg_to = ConfigUtil().get("EMAIL", "msg_to")
        self.passwd = ConfigUtil().get("EMAIL", "passwd")

    def send_email(self, subject, content):
        """

        :param subject: 主题
        :param content:内容
        :return:
        """
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 邮件服务器及端口号
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            logger.info("邮件发送成功")
        except Exception as e:
            logger.error("邮件发送失败")
            logger.error(e)
        finally:
            s.quit()


if __name__ == '__main__':
    EmailSMTP().send_email("测试", "测试")
