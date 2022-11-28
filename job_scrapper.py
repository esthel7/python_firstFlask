from extractors.wwr import extract_wwr_jobs 
# extractors 파일 속 wwr.py 속에서 extract_jobs 함수 불러오기
from extractors.indeed import extract_indeed_jobs
from file import save_to_file

keyword=input("What do you want to search for?")

wwr=extract_wwr_jobs(keyword) # 다른 파일의 함수 활용하기
indeed=extract_indeed_jobs(keyword)
jobs = indeed + wwr #list 형식

save_to_file(keyword, jobs)