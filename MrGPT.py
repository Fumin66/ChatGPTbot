import os
import discord
from dotenv import load_dotenv
import openai

# Discord BotアカウントのトークンとOpenAI APIキーを取得
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# OpenAI APIキーを環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI APIクライアントを作成
openai.api_key = OPENAI_API_KEY
openai.api_base = "https://api.openai.com/v1"

# Discord Botアカウントを作成
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# Botが起動したときに実行されるイベントハンドラー
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# メッセージを受信したときに実行されるイベントハンドラー
@client.event
async def on_message(message):
    # メッセージがBot自身の場合は無視する
    if message.author == client.user:
        return

    # OpenAI APIにメッセージを送信して、ChatGPTからの返信を取得
    prompt = message.content
    response = openai.Completion.create(engine="text-davinci-002",
                                        prompt=prompt,
                                        max_tokens=1024,
                                        n=1,
                                        stop=None,
                                        temperature=0.5)
    reply = response.choices[0].text.strip()

    # ChatGPTからの返信をチャットルームに送信
    await message.channel.send(reply)


# Discord Botアカウントを起動
client.run(TOKEN)
