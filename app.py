from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

#======這裡是呼叫的檔案內容=====
from Method import *
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



# 處理訊息
Todo_dict = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text #自己傳的訊息 , 型態為String
    if  '新增' in msg[0:2]:
        message = IncreaseTodo(msg[2:6],msg[6:],Todo_dict) #(月日,內容,待辦表)
        line_bot_api.reply_message(event.reply_token, message)
    elif '刪除' in msg[0:2]:
        try:
            int(msg[7])
        except ValueError:
            message = TextSendMessage(text="行數必須為整數，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
        try:
            Todo_dict[msg[2:6]]
            message = DeleteTodo(msg[2:6],msg[7],Todo_dict) #(月日,第幾個,待辦表)
            line_bot_api.reply_message(event.reply_token, message)
        except KeyError:
            message = TextSendMessage(text="本日沒有輸入資料，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
    elif '顯示' in msg[0:2]:
        try:
            Todo_dict[msg[2:6]]
            message = ShowTodo(msg[2:6],Todo_dict) #(月日,待辦表)
            line_bot_api.reply_message(event.reply_token, message)
        except KeyError:
            message = TextSendMessage(text="本日沒有輸入資料，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
    elif 'Help' in msg:
        message = Help_template()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text="歡迎使用TODO每日待辦機器人，如果不知道如何使用請輸入Help。")
        line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
