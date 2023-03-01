from chatParser import json_chat_parser

ch = json_chat_parser(r"C:\Users\Ilia-\Downloads\Telegram Desktop\ChatExport_2023-03-01\result.json")
res = ch.get_chat_array()
for c in res:
    print(c)