from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
from bs4 import BeautifulSoup
import random

def sign(thing):
    random_number = random.randrange(60)

    url = f"https://qiangua.temple01.com/qianshi.php?t=fs60&s={random_number}"

    html = requests.get(url)
    html.encoding = "utf-8"

    sp = BeautifulSoup(html.content,"html.parser")

    title1 = sp.find_all("div",class_="fs_poetry_w_top")[0].text
    title2 = sp.find_all("div",class_="fs_poetry_w_top")[1].text
    title3 = sp.find_all("div",class_="fs_poetry_w_top")[2].text.split("\t")[3].split("\n")[0].replace(" ","\n")
    title4 = sp.find_all("div",class_="fs_poetry_w_top")[2].text.split("\t")[3].split("\n")[1]
    main = sp.find("div",class_="fs_poetry_w_text").text
    explain1 = sp.find("div",class_="fs_box fs_left").text.split("\t")[0]
    explain2 = sp.find_all("div",class_="fs_box fs_left")[1].text.split("\t")[0]

    msg = (f"""{title1}

{title2}
{title3}
{title4}
      
籤詩
{main}

語譯
{explain1}

籤意
{explain2}
""")

    return msg

app = Flask(__name__)

line_bot_api = LineBotApi('30fHYzc70eBZEscXrgWyuW0QQMPVGPd4R+CLHhdJAeokJrgn5OlH+TxOcfAzdvxErPxRtvmc6kDr5gvrrm31urWPPayGhThQvwbZ0E79cWH+8M2pjXbtiAgzvwoHX+BcHRnozscUh8i6LIZaUU1zZAdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('b2a58c0974beadd965204bda652ced11')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sign(event.message.text)))


if __name__ == "__main__":
    app.run()
