from requests import get # requests 모듈에서 get(웹사이트 열기)을 사용
from bs4 import BeautifulSoup # bs4 모듈에서 beautifulSoup(html 코드 추출)을 사용

def get_page_count(keyword):
    base_url="https://kr.indeed.com/jobs?q="
    response=get(f"{base_url}{keyword}") #f"{base_url}{keyword}" = base_url+keyword

    if response.status_code!=200:
        print('error',response.status_code)
    else:
        soup=BeautifulSoup(response.text, "html.parser")
        #response.text는 response 페이지의 모든 html
        #html.parser 입력해서 변수 soup에게 html 보낸다고 알리기

        pagination=soup.find("ul",class_="pagination-list") #해당 페이지의 페이지 수(footer의 1,2,3,... 등등)
        
        if pagination==None: #page가 1개
            return 1
        
        pages=pagination.find_all("li",recursive=False)
        #모든 li 정보 중 ul 태그 바로 아래의 li 태그만 얻기 위해 recursive=False (기본은 True라 모든 li 추출됨)
        count=len(pages)

        if count>=5: #해당 페이지에서 나타내는 최대 페이지수가 5
            return 5
        else:
            return count

def extract_indeed_jobs(keyword):
    pages=get_page_count(keyword)
    results=[]

    for page in range(pages):
        base_url="https://kr.indeed.com/jobs"
        response=get(f"{base_url}?q={keyword}&start={page*10}") #f"{base_url}{keyword}" = base_url+keyword
        # start=~~는 해당 페이지의 주소 규칙을 따른 것

        if response.status_code!=200:
            print('error',response.status_code)
        else:
            soup=BeautifulSoup(response.text, "html.parser")
            #response.text는 response 페이지의 모든 html
            #html.parser 입력해서 변수 soup에게 html 보낸다고 알리기

            job_list=soup.find("ul", class_="jobsearch-ResultsList")
            jobs=job_list.find_all('li', recursive=False) 
            #모든 li 정보 중 ul 태그 바로 아래의 li 태그만 얻기 위해 recursive=False (기본은 True라 모든 li 추출됨)

            for job in jobs:
                zone=job.find("div", class_="mosaic-zone")
                if zone==None: #zone에 mosioc-zone class가 없다면 job 관련 li(원하는 li)
                    
                    # h2=job.find("h2", class_="jobTitle")
                    # a=h2.find("a") #h2태그 안에 a태그가 있음
                    anchor=job.select_one("h2 a") #위의 두줄과 동일, 그냥 select쓰면 h2 아래 모든 a 태그 추출
                    
                    title=anchor['aria-label'] #a태그 속 aria-label 속성 내용 추출
                    link=anchor['href']

                    company=job.find("span", class_="companyName")
                    location=job.find("div", class_="companyLocation")

                    job_data={
                        'link' : f"https://kr.indeed.com{link}",
                        'company' : company.string.replace(","," "), #,가 있다면 ,를 공백으로 대체
                        #string 붙여주면 태그 형식이 아니라 안의 값만 추출
                        'location' : location.string.replace(","," "),
                        'position' : title
                    }

                    results.append(job_data)
        return results