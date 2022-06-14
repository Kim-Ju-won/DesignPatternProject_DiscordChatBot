import discord
from discord.ext import commands
from crawler import EnglishCrawler, FacadeEnglishCrawler

class English_command_handler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # 명령어가 올바르게 실행될 수 있는지 체크 
    @commands.Cog.listener()
    async def on_ready(self):
        print("English Command Handler is Ready")
    
    @commands.command(name ="번역", description = "학교 글을 출력해줍니다!")
    async def english(self, ctx, *args):
        keyword = " ".join(args)
        # 크롤러 생성뒤, Facade Pattern으로 해당 함수를 수행할 수 있도록 해줌
        eng = EnglishCrawler(keyword)
        translate= FacadeEnglishCrawler(eng)
        text = translate.crawlData()
        data = "원문: "+keyword+"\n"+"번역결과: "+text
        embed = discord.Embed(title = f"<번역결과>", description = data, color = discord.Color.blue())
        await ctx.send(embed = embed)


# 클라이언트에 해당 명령어 추가
def setup(client):
    client.add_cog(English_command_handler(client))