import base64
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import aiosmtplib

from pasteme import config


def format_addr(name='pasteme', addr=config.EMAIL_ADDRES):
    return formataddr((Header(name, 'utf-8').encode(), addr))


async def send_email(to_address, username):
    code = base64.b64encode(username.encode()).decode()
    msg = MIMEText(f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>pasteme</title>
            <meta charset="utf-8"/>
        </head>
        <body>
            <h1>欢迎注册 pasteme</h1>
            <a href="http://limyel.com:7383/users/checkout/{code}">点击验证您的账号</a>
        </body>
    </html>
    """, 'html', 'utf-8')
    msg['From'] = format_addr()
    msg['To'] = format_addr(name=f'{username} ', addr=to_address)
    msg['Subject'] = Header('pasteme 注册验证', 'utf-8').encode()

    await aiosmtplib.send(msg, sender=config.EMAIL_ADDRES, recipients=[to_address], hostname=config.EMAIL_SERVER,
                          port=config.EMAIL_PORT, username=config.EMAIL_ADDRES, password=config.EMAIL_PASSWORD, use_tls=True)
