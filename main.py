from flask import Flask, render_template, request, redirect, send_file
#flask, templates폴더의 내용(꼭 'templates' 이름의 폴더 & main.py와 동일위치)
#request는 브라우저가 웹사이트에 가서 콘텐츠를 요청하는것, redirect는 해당 url로 이동시키기, send_file은 파일 보내기
from extractors.wwr import extract_wwr_jobs # extractors 파일 속 wwr.py 속에서 extract_jobs 함수 불러오기
from extractors.indeed import extract_indeed_jobs
from file import save_to_file #동일 위치의 file.py에서 save_to_file 함수 불러오기

app=Flask("JobScrapper") #flask를 JobScrapper이름의 app으로 시작

db={} #서버가 켜져있을 때만 정보 유지

@app.route("/") #페이지 사용자가 해당 url접속하면 바로 아래 함수 실행하도록
def home(): # @app.route 바로 아래 위치해야함
    return render_template("home.html", name="esthel") #페이지에 home.html 내용 출력됨

@app.route("/search")
def search():
    keyword=request.args.get("keyword") #request.args는 작성한 form내용인 keyword가 들어있음

    if keyword == None: #keyword가 없는 것은 잘못된 접근(url 직접 입력 등)
        return redirect("/") #해당 url로 보내기

    if keyword in db: #db에 이미 있는 경우 기존 데이터 출력
        jobs=db[keyword]
    else:
        wwr=extract_wwr_jobs(keyword) # 다른 파일의 함수 활용하기
        indeed=extract_indeed_jobs(keyword)
        jobs = indeed + wwr #list 형식

        db[keyword]=jobs #db에 정보 저장

    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword=request.args.get("keyword")

    if keyword==None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"search?keyword={keyword}")

    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True) #as_attachment=True는 다운로드되도록

app.run("0.0.0.0") #서버와 연결