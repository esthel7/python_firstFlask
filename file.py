def save_to_file(file_name, jobs):

    file=open(f"{file_name}.csv", "w", encoding='UTF-8') # w는 write, {file_name}.csv가 생성됨
    file.write("Position,Company,Location,URL\n") #파일에 해당 내용 쓰기
    #csv파일에서 ,는 분할자 역할로 매우 중요

    for job in jobs:
        file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n") 
        #jobs에서의 dictionary 값

    file.close()