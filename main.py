from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    if "バカ" in user_msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="不適切な言葉は使わないでください"))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="メッセージ受け取りました！"))

if __name__ == "__main__":
    app.run()