from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

#======這裡是呼叫的檔案內容=====
from method import *
#======這裡是呼叫的檔案內容=====


#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('t2lQMimmywJibEzVyYYMCvvMl7BWNPwns7TE5NG2D/6kpXWJDntbpTGkpRWecvAH246KpKyEfmMOj/B1KAO/XumLpKNvkAwsIocxHeqE78vqMWXjn7XD2w3O767GjuCS3XlSF69FvNR/QlwBImbwJAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e0b12184361507bbeb6cc1d7549678cd')


# 監聽所有來自 /callback 的 Post Request
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

# 歡迎訊息
@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入 這個專案是check物理習題做出來的')
    line_bot_api.reply_message(event.reply_token, message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text #自己傳的訊息 , 型態為String

    """
     介面呼叫UI
     歡迎介面
     print 用什麼方式找習題呢
    """
    

    """
    1.章節
    印出現有章節
    輸入章節
    印出全部

    輸入標籤
    印出標籤
    """

    """
    2.習題名稱
    印出現有習題名稱
    輸入習題名稱然後print
    """

    """
    3.標籤
    印出現有標籤
    輸入標前然後print
    """
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
