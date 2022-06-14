# Facade Pattern : 크롤러 호출시 내부의 기능을 가리는 용도
# Template Method Pattern: 유사한 기능을 가진 함수를 아래서 추가로 구현하는 용도 
# Proxy Pattern 
# Builder Pattern을 적용하여 크롤러 API를 구현함
from bs4 import BeautifulSoup
import requests
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Template Method Pattern 
class AbstractCralwer:

    # Proxy Pattern을 활용한 크롤러
    def checkdate(self):
        return datetime.date.today()
    # 동적 크롤링이냐 정적 크롤링인지에 따라서 필요에 의해 하위클래스에서 구현함
    # Template Method 
    def startDriver(self): 
        pass
    # Template Method 
    def loadPage(self): 
        pass
    # Template Method 
    def getData(self):
        pass
    # Template Method 
    def quitDriver(self):
        pass

# 영어번역
class EnglishCrawler:

    def __init__(self, keyword):
        self.driver = None
        self.papago_url = None
        self.keyword = keyword
        self.txt = ""

    def startDriver(self): 
        chrome_driver = ChromeDriverManager().install()
        service = Service(chrome_driver)
        self.driver = webdriver.Chrome(service=service)
    # 파파고 페이지 접속
    def loadPage(self): 
        papago_url = 'https://papago.naver.com/'
        self.driver.get(papago_url)
        # 페이지 접속 시간동안 대기
        time.sleep(3)
 
    def getData(self):
        # 입력 창에 단어 입력
        input_keyword = self.driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")
        input_keyword.send_keys(self.keyword)
        
        button = self.driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")
        button.click()
        time.sleep(2)

        # 번역 결과 저장
        self.text = self.driver.find_element(By.CSS_SELECTOR, "div#txtTarget").text
        return self.text

    def quitDriver(self):
        self.driver.close()

# AI 교육원 공지글 크롤링 
class AIunivCrawler(AbstractCralwer):
    # 생성할 때 홈페이지 주소를 넣어둠
    def __init__(self):
        self.AIuniv_url = 'http://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=129898191&siteId=soft&menuType=T&uId=9&sortChar=A&linkUrl=06-3.html&mainFrame=right'
        self.soup = ""
        self.data = ""

    # 페이지 로드
    def loadPage(self):
        url = requests.get(self.AIuniv_url)
        self.soup = BeautifulSoup(url.text, 'html.parser')

    # 학교 공지글에 추가된 게시글 제목 반환
    def getData(self):
        # 오늘 날짜 기록하여 저장
        f=open('AIcrawlerchecker.txt', 'w')
        f.write(str(self.checkdate())+"\n")
        # div#pageRightT태그를 찾아서 저장
        box = self.soup.find('div',{'id':'pageRightT'})
        titles = box.find_all('a')

        title_show = []
        for title in titles :
            if len(title.text.strip()) > 3:
                title_show.append(title.text.strip())

        self.data = title_show
        for data in title_show: 
            data=data +"\n"
            f.write(data)
        f.close()
        return title_show
        
# 한국외대 컴공학부 공지글 크롤링
class HufsCrawler(AbstractCralwer): 
    # 생성할 때 홈페이지 주소를 넣어둠
    def __init__(self):
        self.hufs_url = 'https://computer.hufs.ac.kr/ces/882/subview.do'
        self.soup = ""
        self.data = ""

    # 페이지 로드
    def loadPage(self):
        url = requests.get(self.hufs_url)
        self.soup = BeautifulSoup(url.text, 'html.parser')

    # 학교 공지글에 추가된 게시글 제목 반환
    def getData(self):
        # 오늘 날짜 기록하여 저장
        f=open('HUFScrawlerchecker.txt', 'w')
        f.write(str(self.checkdate())+"\n")
        # div#scroll-table태그를 찾아서 저장
        box = self.soup.find('div',{'class':'scroll-table'})
        titles = box.find_all('strong')

        title_show = []
        for title in titles :
            if len(title.text.strip()) > 3:
                title_show.append(title.text.strip())

        self.data = title_show
        for data in title_show: 
            data=data +"\n"
            f.write(data)
        f.close()
        return title_show

# 인턴 공지글 크롤링
class InternshipCrawler(AbstractCralwer): 
    # 생성할 때 홈페이지 주소를 넣어둠
    def __init__(self):
        self.intern_url = 'https://linkareer.com/list/intern'
        self.soup = ""
        self.data = ""

    # 페이지 로드
    def loadPage(self):
        url = requests.get(self.intern_url)
        self.soup = BeautifulSoup(url.text, 'html.parser')
    # 학교 공지글에 추가된 게시글 제목 반환
    def getData(self):
        # 오늘 날짜 기록하여 저장
        f=open('Interncrawlerchecker.txt', 'w')
        f.write(str(self.checkdate())+"\n")
        # 관련 데이터 추출 
        box = self.soup
        titles = box.find_all('p')

        # 회사, 인턴십이름, 인턴 종류, 지역, 기한, 차례로 입력
        company = []
        for i in range(15,len(titles),15) :
            company.append(titles[i].text.strip())
        job =[]
        for i in range(16,len(titles),15) :
            job.append(titles[i].text.strip())
        job_type = []
        for i in range(17,len(titles),15) :
            job_type.append(titles[i].text.strip())
        region = []
        for i in range(18,len(titles),15) :
            region.append(titles[i].text.strip())
        date = []
        for i in range(19,len(titles),15) :
            date.append(titles[i].text.strip())

        for i in range(len(company)): 
            data=company[i]+"|"+job[i]+"|"+job_type[i]+"|"+region[i]+"|"+date[i]+"\n"
            f.write(data)
        f.close()
        return company, job, job_type, region, date

# Proxy Pattern - ProxyPattern을 적용할 뼈대
class subjectCrawler : 
    def __init__(self, crawler:AbstractCralwer):
        pass

    def crawlData(self):
        pass


# Proxy Pattern 적용 : 같은 날짜에 출력을 할 수 있도록 함수 구현
class ProxyAIcrawler(subjectCrawler):
    def __init__(self, crawler:AbstractCralwer):
        self.crawler = crawler

    def crawlData(self):
        # 같은 날짜에 호출하였으면, 같은 결과 출력
        check = False
        for filename in os.listdir('./'):
            if 'AIcrawlerchecker.txt' in filename:
                f = open(filename,"r")
                date = f.readline()
                if date != str(datetime.date.today()):
                    check = True
                else : 
                    f.close()
                
        data =[]
        if check==True :
            while True:
                line = f.readline()
                if not line: break 
                data.append(line)
            f.close()
        else : # 날짜가 다른 경우 위임받은 크롤러의 크롤링 진행(heavy job)
            self.crawler.loadPage()
            data = self.crawler.getData()
        return data

class ProxyHUFscrawler(subjectCrawler):
    def __init__(self, crawler:AbstractCralwer):
        self.crawler = crawler

    def crawlData(self):
        # 같은 날짜에 호출하였으면, 같은 결과 출력
        check = False
        for filename in os.listdir('./'):
            if 'HUFSscrawlerchecker.txt' in filename:
                f = open(filename,"r")
                date = f.readline()
                if date != str(datetime.date.today()):
                    check = True
                else : 
                    f.close()
        data =[]
        if check==True :
            while True:
                line = f.readline()
                if not line: break 
                data.append(line)
            f.close()
        else : # 날짜가 다른 경우 위임받은 크롤러의 크롤링 진행(heavy job)
            self.crawler.loadPage()
            data = self.crawler.getData()
        return data

class ProxyInternshipCrawler(subjectCrawler):
    def __init__(self, crawler:AbstractCralwer):
        self.crawler = crawler

    def crawlData(self):
        # 같은 날짜에 호출하였으면, 같은 결과 출력
        check = False
        for filename in os.listdir('./'):
            if 'Interncrawlerchecker.txt' in filename:
                f = open(filename,"r")
                date = f.readline()
                if date != str(datetime.date.today()):
                    check = True
                else : 
                    f.close()
        data =[]
        if check==True :
            company=[]
            job=[]
            job_type=[]
            region=[]
            date=[] 
            while True:
                line = f.readline()
                if not line: break 
                c,j,t,r,d= line.split("|")
                company.append(c)
                job.append(j)
                job_type.append(t)
                region.append(r)
                date.append(d)
            f.close()
            return company,job,job_type,region,date
        else : # 날짜가 다른 경우 위임받은 크롤러의 크롤링 진행(heavy job)
            self.crawler.loadPage()
            data = self.crawler.getData()
        return data

# Facade Pattern 적용 : 정적 크롤링을 하는 클래스의 복잡한 내부 내용을 숨겨 챗봇에서 간단한 인터페이스로 활용할 수 있게 해줌
# polymorphism을 적용하여 비슷한 로직을 가지고 있는 HufsCrawler와 AIunivCrawler를 호출하여 활용할 수 있음. 
class FacadeSoupCrawler(subjectCrawler):
    def __init__(self, crawler:AbstractCralwer):
        self.crawler = crawler

    def crawlData(self):
        self.crawler.loadPage()
        data = self.crawler.getData()
        return data

# Facade Pattern 적용 : 정적 크롤링을 하는 클래스의 복잡한 내부 내용을 숨겨 챗봇에서 간단한 인터페이스로 활용할 수 있게 해줌
# polymorphism을 적용하여 비슷한 로직을 가지고 있는 HufsCrawler와 AIunivCrawler를 호출하여 활용할 수 있음. 
class FacadeEnglishCrawler(subjectCrawler):
    def __init__(self, crawler:AbstractCralwer):
        self.crawler = crawler

    def crawlData(self):
        self.crawler.startDriver()
        self.crawler.loadPage()
        data = self.crawler.getData()
        self.crawler.quitDriver()
        return data

