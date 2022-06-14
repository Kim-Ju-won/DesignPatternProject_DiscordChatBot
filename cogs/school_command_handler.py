import discord
from discord.ext import commands
from crawler import ProxyAIcrawler, AIunivCrawler, ProxyHUFscrawler, HufsCrawler

class school_command_handler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # 명령어가 올바르게 실행될 수 있는지 체크 
    @commands.Cog.listener()
    async def on_ready(self):
        print("School Command Handler is Ready")
    
    @commands.command(name ="전공 공지글", description = "AI 교육원 및 공학과 글을 출력해줍니다!")
    async def school(self, ctx):
        # 크롤러 생성뒤, Facade Pattern으로 해당 함수를 수행할 수 있도록 해줌
        AI = AIunivCrawler()
        AI_info = ProxyAIcrawler(AI)
        data = AI_info.crawlData()
        # 상위 5개만 출력
        for i in range(5):
            embed = discord.Embed(title = f"<AI교육원 {i+1}번째 게시글>", description = data[i], color = discord.Color.blue())
            await ctx.send(embed = embed)

        # 크롤러 생성뒤, Facade Pattern으로 해당 함수를 수행할 수 있도록 해줌
        HUFS = HufsCrawler()
        HUFS_info = ProxyHUFscrawler(HUFS)
        data = HUFS_info.crawlData()
        # 상위 5개만 출력
        for i in range(5):
            embed = discord.Embed(title = f"<한국외대 컴퓨터공학과 {i+1}번째 게시글>", description = data[i], color = discord.Color.blue())
            await ctx.send(embed = embed)

# 클라이언트에 해당 명령어 추가
def setup(client):
    client.add_cog(school_command_handler(client))