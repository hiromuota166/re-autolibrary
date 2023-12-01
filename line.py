# LINEに通知を送る関数

import requests

# APIのURLとトークン
url = "https://notify-api.line.me/api/notify"

access_token = [
  "qXB6gOOOu9SvIPaOSFP6HzPQcnNylgXBe0A49yIBp2q",#re:図書館予約
]

message = "こーとがあいてるよ！"

def send_line_notify(message):
  for token in access_token:
    headers = {"Authorization" : "Bearer "+ token}
    send_data = {"message" :  message}
    result = requests.post(url, headers = headers, data = send_data)
    print(result)

if __name__ == "__main__":
  send_line_notify("デフォルト")