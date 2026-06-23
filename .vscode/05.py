"""
第一个AI API调用程序（多轮对话版 - WebSocket X2版）
课程：《人工智能应用开发技术》
模块：一、AI应用开发入门
"""

import json
import websocket
import datetime
import hashlib
import base64
import hmac
from urllib.parse import urlencode

# ===== API配置（X2）=====
url = "wss://spark-api.xf-yun.com/x2"

APPID = "03824288"
APIKey = "965d41e9a5cdc07193f844d4d0b4f3e7"
APISecret = "NmQyMDc1ODc5NzgxMzE1NThhYzJiN2Iw"

# ===== 对话历史 =====
chat_history = []


# ===== 生成鉴权URL =====
def create_url():
    host = "spark-api.xf-yun.com"
    path = "/x2"

    now = datetime.datetime.utcnow()
    date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
    signature_sha = hmac.new(
        APISecret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()

    signature = base64.b64encode(signature_sha).decode()

    authorization_origin = f'api_key="{APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()

    params = {
        "authorization": authorization,
        "date": date,
        "host": host
    }

    return url + "?" + urlencode(params)


# ===== 获取AI响应 =====
def get_ai_response(question):
    chat_history.append({"role": "user", "content": question})

    ws_url = create_url()
    result_text = ""

    def on_message(ws, message):
        nonlocal result_text
        data = json.loads(message)

        # 👉 调试用（建议第一次运行保留）
       # print("收到：", data)

        if "payload" in data:
            try:
                text_list = data["payload"]["choices"]["text"]

                for item in text_list:
                    if "content" in item:
                        result_text += item["content"]

            except Exception as e:
                print("解析错误：", e)

        # status=2 表示结束
        if data.get("header", {}).get("status") == 2:
            ws.close()

    def on_error(ws, error):
        print("错误：", error)

    def on_close(ws, a, b):
        pass

    def on_open(ws):
        data = {
            "header": {
                "app_id": APPID
            },
            "parameter": {
                "chat": {
                    "domain": "spark-x",   
                    "temperature": 0.5,
                    "max_tokens": 2048,
                    "thinking": {
                        "type": "disabled"   
                    }
                }
            },
            "payload": {
                "message": {
                    "text": chat_history
                }
            }
        }

        ws.send(json.dumps(data))

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open
    ws.run_forever()

    chat_history.append({"role": "assistant", "content": result_text})

    return result_text


# ===== 主程序 =====
if __name__ == "__main__":
    print("讯飞星火AI多轮对话（WebSocket X2版）")
    print("输入 '退出' 或 'quit' 可结束对话")
    print("-" * 50)

    while True:
        question = input("你：")

        if question.strip().lower() in ["退出", "quit", "exit"]:
            print("AI：再见！对话结束～")
            break

        if not question.strip():
            print("AI：请输入有效问题哦～")
            continue

        answer = get_ai_response(question)

        print("\nAI：", answer)
        print("-" * 50)