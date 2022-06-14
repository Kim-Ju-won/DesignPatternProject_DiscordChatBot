import discord
from discord.ext import commands
from crawler import InternshipCrawler, ProxyInternshipCrawler

class internship_command_handler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # 명령어가 올바르게 실행될 수 있는지 체크 
    @commands.Cog.listener()
    async def on_ready(self):
        print("InternShip Command Handler is Ready")
    
    @commands.command(name ="인턴", description = "인턴 공지 글을 출력해줍니다!")
    async def internship(self, ctx):
        # 크롤러 생성뒤, Facade Pattern으로 해당 함수를 수행할 수 있도록 해줌
        Internship = InternshipCrawler()
        Internship_info= ProxyInternshipCrawler(Internship)
        company, job, job_type, region, date  = Internship_info.crawlData()
        # 상위 5개만 출력
        
        # 상위 5개만 출력
        for i in range(5):
            data="회사: "+company[i]+"\n인턴 명: "+job[i]+"\n인턴십 종류: "+job_type[i]+"\n지역: "+region[i]+"\n날짜: "+date[i]
            embed = discord.Embed(title = f"<인턴관련 {i+1}번째 게시글>", description = data, color = discord.Color.blue())
            await ctx.send(embed = embed)

# 클라이언트에 해당 명령어 추가
def setup(client):
    client.add_cog(internship_command_handler(client))