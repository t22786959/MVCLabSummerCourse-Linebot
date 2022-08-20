'''
This is my LineBot API
How to Start:
    > Step 0. Go to ./MVCLab-Summer-Course/LineBot/
        > cd ./MVCLab-Summer-Course/LineBot
    > Step 1. Install Python Packages
        > pip install -r requirements.txt
    > Step 2. Run main.py
        > python main.py
Reference:
1. LineBot API for Python
    > https://github.com/line/line-bot-sdk-python
2. Pokemon's reference
    > https://pokemondb.net/pokedex/all
3. Line Developer Messaging API Doc
    > https://developers.line.biz/en/docs/messaging-api/
'''
import os
import re
import json
import random
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv() # Load your local environment variables


CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

'''
For first testing, you can comment the code below after you check your linebot can send you the message below
'''
CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID
# My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='Welcome to my pokedex !')) # Push a testing message



# Line Developer Webhook Entry Point
@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# All message events are handling at here !
@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    global my_pokemons
    oper=['+','-','*','/']
    # Split message by white space
    recieve_message = str(event.message.text).split(' ')
    if any(elem.isalpha() for elem in recieve_message[0]):
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(text='There is some invalid character in your command !')
        )
    elif recieve_message[1] in oper:
        if any(elem.isalpha() for elem in recieve_message[2]):
            ret='There is some invalid character in your command !'
        elif recieve_message[1]==oper[0]:
            ret=int(recieve_message[0])+int(recieve_message[2])
        elif recieve_message[1]==oper[1]:
            ret=int(recieve_message[0])-int(recieve_message[2])
        elif recieve_message[1]==oper[2]:
            ret=int(recieve_message[0])*int(recieve_message[2])
        elif recieve_message[1]==oper[3]:
            if int(recieve_message[2])==0:
                ret='Division by zero !'
            else:
                ret=int(recieve_message[0])/int(recieve_message[2])
       
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(text=str(ret))
        )
    else:
        emoji = [
    {
        "index": 28,
        "productId": "5ac221ca040ab15980c9b449",
        "emojiId": "018"
    }
]
    message = TextSendMessage(text='Your operator isn\'t defined $', emojis=emoji)
    My_LineBotAPI.reply_message(
            event.reply_token,
            message
        )



    
# Line Sticker Class
class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id

'''
See more about Line Sticker, references below
> Line Developer Message API, https://developers.line.biz/en/reference/messaging-api/#sticker-message
> Line Bot Free Stickers, https://developers.line.biz/en/docs/messaging-api/sticker-list/
'''
# Add stickers into my_sticker list
my_sticker = [My_Sticker(p_id='446', s_id='1988'),
     My_Sticker(p_id='789', s_id='10857'), My_Sticker(p_id='789', s_id='10877'),
     My_Sticker(p_id='6325', s_id='10979904'), My_Sticker(p_id='6325', s_id='10979906'),
     My_Sticker(p_id='6325', s_id='10979908'), My_Sticker(p_id='6325', s_id='10979910')
     ]

# Line Sticker Event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ran_sticker = random.choice(my_sticker)
    # Reply Sticker Message
    message=[]
    message.append(TextSendMessage(text='That\'s a nice sticker !'))
    message.append(StickerSendMessage(
            package_id= ran_sticker.packageID,
            sticker_id= ran_sticker.stickerID
        )
    )
    My_LineBotAPI.reply_message(
        event.reply_token,
        message
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)
