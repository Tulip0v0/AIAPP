import gradio as gr
import websocket
import hashlib
import hmac
import base64
import json
from datetime import datetime
from urllib.parse import urlencode

# -------------- 配置 ----------------
APP_ID = "7fdc7acf"
API_KEY = "9d0d04fccb559bd09cab18780d508613"
API_SECRET = "NWU4NzI4MDFkMmJlYTRmYjViMzA2ODVh"
DOMAIN = "lite"
VERSION = "v1.1"

# -------------- 鉴权 ----------------
def get_auth_url():
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nGET /v1.1/chat HTTP/1.1"
    sha = hmac.new(API_SECRET.encode(), signature_origin.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(sha).decode()
    auth = f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authb = base64.b64encode(auth.encode()).decode()
    query = urlencode({"authorization": authb, "date": date, "host": "spark-api.xf-yun.com"})
    return f"wss://spark-api.xf-yun.com/v1.1/chat?{query}"

# -------------- 聊天函数 ----------------
def chat_with_ai(message, history):
    url = get_auth_url()
    ws = websocket.create_connection(url)
    data = {
        "header": {"app_id": APP_ID},
        "parameter": {"chat": {"domain": DOMAIN}},
        "payload": {"message": {"text": [{"role": "user", "content": message}]}}
    }
    ws.send(json.dumps(data))
    res = ""
    while True:
        msg = json.loads(ws.recv())
        if msg["header"]["code"] != 0:
            return "错误：" + msg["header"]["message"]
        res += msg["payload"]["choices"]["text"][0]["content"]
        if msg["header"]["status"] == 2:
            break
    ws.close()
    return res

# -------------- 界面 ----------------
demo = gr.ChatInterface(
    fn=chat_with_ai,
    title="AI对话机器人",
    description="我是你的AI助手"
)

demo.launch()