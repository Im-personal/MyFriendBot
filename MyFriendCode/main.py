from chatParser import html_chat_parser

chat = html_chat_parser('C:/Users/Ilia-/Downloads/Telegram Desktop/ChatExport_2023-02-27/messages.html')
for msg in chat.messages:
    print(f"{msg.user.name}: {msg.text}")
