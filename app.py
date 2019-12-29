# !/usr/bin/python
# coding:utf-8

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======call file data =====
from message import *
from dictionary import *
#======call file data =====

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ClFzK4Oisy25R05SDvQ2+cSqy8vVf3q3AJdW/cuag6r+szNuULYmcuKHDJfZ55RwdsIpec6z4l9ClYpdRf08c+WmBHfc5lqkGSFZm7CagQUvU6E+AKi1QK3erH5fkTUxOWCNYTJw+gaDYcAh43qZmAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6c7a00aa1af3d317cd64cd70ee60c92b')

# supervise all /callback from Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    df = dic_scraping_bot(msg)
    if df == None:
        message = TextSendMessage(text='查無此字')
        line_bot_api.reply_message(event.reply_token, message)  
    elif '發音' in msg:
        message = Confirm_Pronounce(df['name'])
        line_bot_api.reply_message(event.reply_token, message)
    elif '英式' in msg:
        message = Pronounce(df['data'], '英式')
        line_bot_api.reply_message(event.reply_token, message)
    elif '美式' in msg:
        message = Pronounce(df['data'], '美式')
        line_bot_api.reply_message(event.reply_token, message)
    elif '例句' in msg:
        message = Example(df['data'])
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = Confirm_Word(df['name'],df['data'])
        line_bot_api.reply_message(event.reply_token,message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
