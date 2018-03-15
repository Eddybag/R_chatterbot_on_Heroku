from flask import Flask
from flask import request
from pymessenger import Bot 
import os
import sys

from chatterbot import ChatBot
chatterbot = ChatBot("DinDin")
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.comparisons import levenshtein_distance



PAGE_ACCESS_TOKEN = 'EAAcsDZC6g5p4BAO6wrJP0cB86ZCrW1v7zbfdgTa1QSXOozut9cBXGBTQX5yvZCgKV968wKczkGiaT99tgwspCiime1v8e9mDKKrKR8zqpMekZC3AN5EPwFgqhBmQL996QYCtLdm4jcQ2BGp7MumesxqayVZANVCbyP05Fi1tzMwZDZD'
bot = Bot(PAGE_ACCESS_TOKEN)

app = Flask(__name__) 

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'hello':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # chatterbot = ChatBot(
    # 'DinDin',
    # # storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    # logic_adapters=
    #     [{
    #         "import_path": "chatterbot.logic.BestMatch",
    #         "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
    #         "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
    #     }],
    # input_adapter='chatterbot.input.VariableInputTypeAdapter',
    # output_adapter="chatterbot.output.OutputAdapter",
    # output_format="text",
    # database='chatterbot-database')

    # chatterbot.set_trainer(ListTrainer)


    
 
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:         # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                            # bot.send_text_message(sender_id, 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                    else:
                        messaging_text = 'no text'
                    # print(messaging_text)  
                    response = str(botDindin(str(messaging_text)))

                    bot.send_text_message(sender_id,response)   
					    # Echo
    return "ok", 200


def botDindin(input):
    bot = ChatBot('Norman', 
        logic_adapters=[    
       {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        ],
    
    preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    statement_comparison_function=levenshtein_distance)    
    bot.set_trainer(ListTrainer)
    bot.train(['hi','請問需要甚麼幫助?'])
    bot.train(['Hey','需要什麼幫忙嗎?'])
    bot.train(['hello','需要我幫忙什麼?'])
    bot.train(['你好','你好, 很高興為您服務'])
    bot.train(['嗨','嗨, 需要我幫忙什麼?'])
    bot.train(['我想找一瓶 (雪碧)','以下是 雪碧 的詳細資料,價格為 30 元, 590 毫升, 內含熱量為 230 卡'])
    bot.train(['我想找一瓶 (茶裏王)','好, 幫你查一下 茶裏王, 以下是 你要的詳細資料,價格為 25 元, 590 毫升, 內含熱量為 230 卡'])
    bot.train(['我想找一罐 (可樂) (cola)','沒問題, 以下是 可樂 的詳細資料,價格為 30 元, 380 毫升, 內含熱量為 222 卡'])
    bot.train(['我需要找一罐 (伯朗咖啡) (Mr.brown coffee)','好, 馬上幫你查一下,以下是 伯朗咖啡 Mr.brown coffee 的詳細資料,價格為 30 元, 200 毫升, 內含熱量為 200 卡'])
    bot.train(['我需要一包 (衛生紙)','衛生紙的價格為 30 元'])
    bot.train(['請問 (刮鬍刀) 我需要','好, 馬上幫你查一下,以下是 刮鬍刀 的詳細資料,價格為 20 元'])
    bot.train(['我要找一碗 (阿Q桶麵)','以下是 阿Q桶麵 的詳細資料,價格為 35 元, 內含熱量為 500 卡'])
    bot.train(['我要找一包 (維力炸醬麵)','以下是 維力炸醬麵 的詳細資料,價格為 25 元, 內含熱量為 300 卡'])
    bot.train(["我需要一包 (樂事原味洋芋片) (Lay's Original)",'好的, 以下是 樂事原味洋芋片 的詳細資料,價格為 30 元, 內含熱量為 400 卡'])
    bot.train(['我需要一個 (義美泡芙)','好, 馬上幫你查一下,以下是 義美泡芙 的詳細資料,價格為 40 元, 內含熱量為 250 卡'])
    response = bot.get_response(input)
    
    return response

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True, port=8088)