from extractors.wwr import extract_wwr_jobs 
# extractors 파일 속 wwr.py 속에서 extract_jobs 함수 불러오기
from extractors.indeed import extract_indeed_jobs

keyword=input("What do you want to search for?")

wwr=extract_wwr_jobs(keyword) # 다른 파일의 함수 활용하기
indeed=extract_indeed_jobs(keyword)
jobs = indeed + wwr

file=open(f"{keyword}.csv", "w") # w는 write, {keyword}.csv가 생성됨
file.write("Position,Company,Location,URL\n") #파일에 해당 내용 쓰기
#csv파일에서 ,는 분할자 역할로 매우 중요

for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n") 
    #jobs에서의 dictionary 값

file.close()
