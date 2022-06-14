## DesignPatternProject_DiscordChatBot 
# ChatBot 클래스

import discord
from discord.ext import commands
import os

class school_life_chatbot :
    # 생성자 : token, 명령어의 prefix 초기화, 서버 정보 입력
    def __init__(self):
        self.token = ''
        self.prefix ='!'
        self.intents = discord.Intents.all()

    # startchatbot함수를 통해 token을 불러와 bot실행
    def startchatbot(self):
        # 봇 정보 입력
        client = commands.Bot(command_prefix=self.prefix, intents = self.intents)

        # load_extension 함수를 이용하여 다양한 명령어 처리기 등록
        for filename in os.listdir('./cogs'):
            if '.py' in filename and filename:
                filename = filename.replace('.py', '')
                client.load_extension(f"cogs.{filename}")

        # 텍스트 파일에 토큰일 읽어옴
        with open('token.txt', 'r') as f:
            self.token = f.read()
        # 토큰을 입력하여 봇 실행
        client.run(self.token)