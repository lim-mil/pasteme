from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import aiosmtplib

from pasteme import config


class EmailServer:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.smtp = None

    async def login_email(self):
        try:
            async with aiosmtplib.SMTP(hostname=config.EMAIL_SERVER, port=config.PORT, use_tls=True) as smtp:
                await smtp.login(config.EMAIL_ADDRES, config.EMAIL_PASSWORD)
                self.smtp = smtp
                print(self.smtp)
        except Exception as e:
            import traceback


    def format_addr(self, name='pasteme', addr=config.EMAIL_ADDRES):
        return formataddr((Header(name, 'utf-8').encode(), addr))


EMAIL = EmailServer()


async def send_email(to_address, username):
    msg = MIMEText('hello', 'html', 'utf-8')
    msg['From'] = EMAIL.format_addr()
    msg['To'] = EMAIL.format_addr(name=f'{username} ', addr=to_address)
    msg['Subject'] = Header('pasteme 注册验证', 'utf-8').encode()

    await EMAIL.smtp.send_message(msg)


if __name__ == '__main__':
    pass
