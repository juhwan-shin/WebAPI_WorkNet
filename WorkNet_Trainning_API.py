### 청년취업정책API
### 워크넷 API를 활용함
from lxml import etree
import pymysql
import datetime as dt

def WorkNet_Trainning() :
    conn = pymysql.connect(host='211.55.39.22', port=43306, user='knu', password='Knu_0987!@#', db='test',
                           charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now_date = dt.datetime.now()
    now_date = now_date.strftime('%y-%m-%d %H:%M:%S')
    # Load XML and for Check base data 데이터 개수 파악하기 위함.
    tree = etree.parse("http://openapi.work.go.kr/opi/opi/opia/jynEmpSptListAPI.do?authKey=WNJNO8MC0BQ3O2FB6JED12VR1HJ&returnType=xml")
    root = tree.getroot()

    # Get base data 데이터 개수 파악 한 뒤 파싱할 페이지 체크.
    kids = root.getchildren()
    showItemListCount = 100             # 리스트를 한번에 읽는 개수
    count = int(int(kids[0].text)/100) + 2   # 리스트를 100개 단위로 count 만큼 읽음.

    # Get Main data
    for i in range(1, count) :
        tree = etree.parse("http://openapi.work.go.kr/opi/opi/opia/jynEmpSptListAPI.do?authKey=WNJNO8MC0BQ3O2FB6JED12VR1HJ&returnType=xml&startPage=" + str(i) + "&display=100")
        root = tree.getroot()
        kids = root.getchildren()
        title =""
        intro =""
        background = ""
        department = ""
        source = ""
        content = ""
        target=""
        apply_url=""

        for child in kids[3:] :     # 인덱스 0과 1은 파싱할 필요 없는 부분. Item의 element태그 탐색

            for element in child :
                if element.tag == "busiNm" :
                    title=element.text
                elif element.tag == "dtlBusiNm" :
                    intro = element.text
                elif element.tag == "busiSum" :     # 교육 훈련 관련 프로그램 출력
                    content = element.text
                elif element.tag == "chargerOrgNm":
                    department= element.text
                elif element.tag == "applUrl":
                    apply_url= element.text
                elif element.tag == "detalUrl":
                    source= element.text
                elif element.tag == "edubgEtcCont":
                    background= element.text
                elif element.tag == "empEtcCont":
                    target = element.text
            sql = """insert into employ_information(title, intro, background, department, time, source, category, content, target, apply_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (title, intro, background, department, now_date, source, "교육훈련", content, target, apply_url))
            conn.commit()


def insertDB(self):
    conn = pymysql.connect(host='211.55.39.22', port=43306, user='knu', password='Knu_0987!@#', db='test',
                           charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    if (self.siteVersion == 0):
        df = self.getResult()
        for i in range(len(df)):
            tmp = df['등록일'][0].split('-')
            date = dt.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            date = date.strftime('%y-%m-%d %H:%M:%S')

            now_date = dt.datetime.now()
            now_date = now_date.strftime('%y-%m-%d %H:%M:%S')

            sql = """insert into employ_information(title, intro, background, department, url_link, time, source, category, content, target, apply_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (df['제목'][i], df['담당부서'][i], date, df['조회수'][i], df['첨부링크'][i],
                               "http://www.chuncheon.go.kr/index.chuncheon?menuCd=DOM_000000505003001000&cpath=",
                               "춘천시청", "고시공고", now_date, ""))
            conn.commit()

        print("db insert 완료")
    elif (self.siteVersion == 3):
        df = self.getResult()
        for i in range(len(df)):

            tmp = df['작성일'][0].split('-')
            date = dt.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            date = date.strftime('%y-%m-%d %H:%M:%S')

            now_date = dt.datetime.now()
            now_date = now_date.strftime('%y-%m-%d %H:%M:%S')

            sql = """insert into employ_information(title,  date, hits, file_link, url_link, source, category, time, content) values (%s, %s, %s, %s, %s, %s, %s, %s , %s)"""

            try:
                curs.execute(sql, (
                    df['제목'][i], date, df['조회'][i], df['첨부링크'][i], df['게시물링크'][i], "춘천고용복지센터", "고시공고", now_date, ""))
                conn.commit()
            except pymysql.DataError:
                print(str(i) + "번 데이터는 데이터베이스 형식과 맞지 않습니다.")

        print("db insert 완료")
WorkNet_Trainning()

# (title, intro, content, department, url_link, `time`, source, category, target)