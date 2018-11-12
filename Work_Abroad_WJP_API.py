### 해외일자리 기업 및 구인정보
### 월드잡플러스 API를 활용함
from lxml import etree
import pymysql
import datetime as dt
# 문서에 오류가 있는지 체크하는 함수
def checkError(errorCode) :
    if errorCode != "00" :
        print("xml 문서 접근 오류")
        exit(0)


def Work_Abroad_WJP() :
    # Load XML and for Check base data 데이터 개수 파악하기 위함.
    tree = etree.parse("http://www.worldjob.or.kr/openapi/openapi.do?dobType=1")
    root = tree.getroot()
    conn = pymysql.connect(host='xxx.xx.xx.xx', port=xxxxx, user='xxx', password='xxxxxxxxx', db='test',
                           charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now_date = dt.datetime.now()
    now_date = now_date.strftime('%y-%m-%d %H:%M:%S')

    # Get base data 데이터 개수 파악 한 뒤 파싱할 페이지 체크.
    kids = root.getchildren()
    showItemListCount = 100             # 리스트를 한번에 읽는 개수
    count = int(int(kids[1].text)/showItemListCount) + 1   # pageIndex로 100개 단위로 pageIndex 만큼 읽음.

    # Get Main data
    for i in range(1, count) :
        tree = etree.parse("http://www.worldjob.or.kr/openapi/openapi.do?dobType=1&pageIndex=" + str(i) + "&showItemListCount=100")
        root = tree.getroot()
        kids = root.getchildren()
        title = ""
        gift = ""
        nation = ""
        job = ""
        career = ""
        background=""
        endday = ""
        url_link = ""
        content = ""
        apply_url = ""
        for child in kids[2:] :     # 인덱스 0과 1은 파싱할 필요 없는 부분. Item의 element태그 탐색
            for element in child :
                if element.tag == "rctntcSj" :
                    title = element.text
                elif element.tag == "rctntcSprtQualfCn" :
                    gift = element.text
                elif element.tag == "dsptcNationScd" :
                    nation =  element.text
                elif element.tag == "dsptcKsco" :
                    job= element.text
                elif element.tag == "joDemandCareerStleScd":
                    career = element.text
                elif element.tag == "joDemandAcdmcrScd":
                    background= element.text
                elif element.tag == "rctntcEndDay":
                    endday=element.text
                elif element.tag == "linkUrl":
                    url_link=element.text
                elif element.tag == "directApply":
                    apply_url=element.text
            content = title
            endday = endday.replace("/", "-")
            endday = now_date[0:1] +"-"+ endday[0:5] + " 00:00:00"

            sql = """insert into employ_information(title, gift, nation, job, career, background, endday, `time`, source, category, content, apply_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (title, gift, nation, job, career, background, endday, now_date, url_link, "해외채용", content, apply_url))
            conn.commit()

Work_Abroad_WJP()