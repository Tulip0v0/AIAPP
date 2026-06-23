"""

第一个AI API调用程序

课程：《人工智能应用开发技术》

模块：一、AI应用开发入门

"""



import requests

import json

import os




url = "https://spark-api-open.xf-yun.com/v1/chat/completions"

MAX_HISTORY_TURNS = 10  # 保留最近10轮对话记忆（1轮=用户+AI）

conversation_messages = []



while True:



    #####倪文我打开始h



    # 准备要问的问题

    try:

        question = input("请输入你想问的问题（输入 exit/退出 结束，clear/清空 重置记忆）：").strip()

    except (KeyboardInterrupt, EOFError):

        print("\n已退出聊天。")

        break



    if question.lower() in {"q", "quit", "exit", "退出"}:

        print("已退出聊天。")

        break



    if question.lower() in {"clear", "清空"}:

        conversation_messages.clear()

        print("对话记忆已清空。")

        continue



    if not question:

        print("输入不能为空，请重新输入。")

        continue



    conversation_messages.append(

        {

            "role": "user",

            "content": question

        }

    )

    messages_for_request = conversation_messages[-MAX_HISTORY_TURNS * 2:]



    data = {

            "model": "lite", # 指定请求的模型

            "messages": messages_for_request,

            "tools": [

            {

                "type": "function",

                "function": {

                    "name": "get_current_weather",

                    "description": "返回实时天气",

                    "parameters": {

                        "type": "object",

                        "properties": {

                            "location": {

                                "type": "string",

                                "description": "河北省承德市双桥区",

                            },

                            "format": {

                                "type": "string",

                                "enum": ["celsius", "fahrenheit"],

                                "description": "使用本地区常用的温度单位计量",

                            },

                        },

                        "required": ["location", "format"],

                    }

                }

            }

        ]

        }

    header = {

        "Content-Type": "application/json",

        "Authorization": "Bearer kVwkpAVWyeUCgkONYtoX:jcThWkwJJXIQkofOrQQG" # 注意此处把“123456”替换为自己的APIPassword

    }

    response = requests.post(url, headers=header, json=data)



    # response = requests.post(url, json=payload, headers=headers)



    # 处理响应

    if response.status_code == 200:

        result = response.json()

        # 解析结果（不同平台格式不同）

        answer = result["choices"][0]["message"]["content"]

        conversation_messages.append(

            {

                "role": "assistant",

                "content": answer

            }

        )

        print("\n" + "="*50)

        print("AI的回答：")

        print(answer)

        print("="*50)

    else:

        # 请求失败时撤回本轮用户输入，避免无效问句进入记忆

        if conversation_messages and conversation_messages[-1]["role"] == "user":

            conversation_messages.pop()

        print(f"出错了，错误码：{response.status_code}")

        print(response.text)



    ######你问我打结束