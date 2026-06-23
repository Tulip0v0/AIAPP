"""

第一个AI API调用程序

课程：《人工智能应用开发技术》

模块：一、AI应用开发入门

"""



import requests

import json

import os



# 从本地配置文件读取凭据，避免在代码中明文保存密钥

#



url = "https://spark-api-open.xf-yun.com/v1/chat/completions"



while True:



    #####倪文我打开始h



    # 准备要问的问题

    question = input("请输入你想问的问题：")

    data = {

            "model": "lite", # 指定请求的模型

            "messages": [

                {

                    "role": "user",

                    "content": question

                }

            ],

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

        print("\n" + "="*50)

        print("AI的回答：")

        print(answer)

        print("="*50)

    else:

        print(f"出错了，错误码：{response.status_code}")

        print(response.text)



    ######你问我打结束

