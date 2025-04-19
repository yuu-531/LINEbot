from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, StickerMessage, TextSendMessage
import time

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# ユーザーごとのスタンプ履歴を保存
user_sticker_log = {}

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

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    user_id = event.source.user_id
    now = time.time()

    # ログにユーザーがいなければ初期化
    if user_id not in user_sticker_log:
        user_sticker_log[user_id] = []

    # 現在時刻をログに追加
    user_sticker_log[user_id].append(now)

    # 直近5秒以内のスタンプだけ残す
    user_sticker_log[user_id] = [t for t in user_sticker_log[user_id] if now - t <= 5]

    # 5秒以内に3回以上スタンプ送ってたら警告
    if len(user_sticker_log[user_id]) >= 3:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="スタンプ連投は控えてください！")
        )

if __name__ == "__main__":
    app.run()
