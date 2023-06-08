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

import twstock

twstock.realtime.mock = False

def realtime(stock_id):    
    stock_info = twstock.realtime.get(stock_id)

    if stock_info['success'] == True:
        best_bid_price = stock_info['realtime']['best_bid_price']
        best_bid_volume = stock_info['realtime']['best_bid_volume']
        best_ask_price = stock_info['realtime']['best_ask_price']
        best_ask_volume = stock_info['realtime']['best_ask_volume']

        msg = (f"""{stock_id}即時股價資訊

股票名稱: {stock_info['info']['name']}
股票代碼: {stock_info['info']['code']}
資料時間: {stock_info['info']['time']}
當前股價: {stock_info['realtime']['latest_trade_price']}
開盤價: {float(stock_info['realtime']['open']):.2f}
最高價: {float(stock_info['realtime']['high']):.2f}
最低價: {float(stock_info['realtime']['low']):.2f}
當前交易量: {stock_info['realtime']['trade_volume']}
累積交易量: {stock_info['realtime']['accumulate_trade_volume']}
當前5筆成交價: {float(best_bid_price[0]):.2f}, {float(best_bid_price[1]):.2f}, {float(best_bid_price[2]):.2f}, {float(best_bid_price[3]):.2f}, {float(best_bid_price[4]):.2f}
當前5筆成交量: {int(best_bid_volume[0])}, {int(best_bid_volume[1])}, {int(best_bid_volume[2])}, {int(best_bid_volume[3])}, {int(best_bid_volume[4])}
最佳5筆成交價: {float(best_ask_price[0]):.2f}, {float(best_ask_price[1]):.2f}, {float(best_ask_price[2]):.2f}, {float(best_ask_price[3]):.2f}, {float(best_ask_price[4]):.2f}
最佳5筆成交量: {int(best_ask_volume[0])}, {int(best_ask_volume[1])}, {int(best_ask_volume[2])}, {int(best_ask_volume[3])}, {int(best_ask_volume[4])}
""")

        return msg
    else:
        error = "Data not found"

        return error

app = Flask(__name__)

line_bot_api = LineBotApi('S5nw445xmRrBSubt35PFZ6kFb3pTYd5tkI+Dek4Rycq5+I29Kx6633HDHHN0S3KG9QOdvwGJilf6ujdGs2F2RuqIAH8dSfnP2WKRtBx4jXe7C2GDBqDBYIzFENoe37Ct1bXmwoJsT2EiBhGSPJRPhQdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('04c62a547006bc111ebf5962dfa87eb5')


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
        TextSendMessage(text=realtime(event.message.text)))


if __name__ == "__main__":
    app.run()
