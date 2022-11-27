from requests import get # requests 모듈에서 get(웹사이트 열기)을 사용
from bs4 import BeautifulSoup # bs4 모듈에서 beautifulSoup(html 코드 추출)을 사용

def extract_wwr_jobs(keyword):

    base_url="https://weworkremotely.com/remote-jobs/search?term="

    response=get(f"{base_url}{keyword}") #f"{base_url}{keyword}"==base_url+keyword
    #response= <Response [200]>

    if response.status_code != 200 :
        print('error')

    else:
        results=[]
        soup=BeautifulSoup(response.text, "html.parser")
        #response.text는 response 페이지의 모든 html
        #html.parser 입력해서 변수 soup에게 html 보낸다고 알리기

        jobs=soup.find_all('section',class_="jobs") #section 태그 중 class가 jobs 인 것

        for job_section in jobs:
            job_posts=job_section.find_all('li')
            job_posts.pop(-1) #맨 뒤 한 개의 리스트만 삭제

            for post in job_posts:
                anchors=post.find_all('a')
                anchor=anchors[1] #두번째 a 태그 (0부터 시작)
                link=anchor['href'] #a 태그의 href 부분만 추출

                company, kind, region = anchor.find_all('span',class_='company') 
                #span 태그의 company class인 것은 3가지 항목이 있고, 각자 지정
                title=anchor.find('span',class_='title') #find_all은 모든 항목, find는 첫번째만

                job_data={
                'link' : f"https://weworkremotely.com{link}", #link는 상대경로로 나오므로 https~ 추가
                'company' : company.string.replace(","," "), #,가 있다면 ,를 공백으로 대체
                #string 붙여주면 태그 형식이 아니라 안의 값만 추출
                'location' : region.string.replace(","," "),
                'position' : title.string.replace(","," ")
                }
                results.append(job_data)

        return results