from flask import Flask, render_template, request
from gmarket_scraper import get_gmarket_reviews
from coupang_scraper import get_coupang_reviews
from review_analyzer import analyze_reviews_in_one_call
from ai_detector import filter_reviews_by_ai

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    analysis_result = None 
    reviews = []
    filter_info = None

    if request.method == "POST":
        url = request.form.get("url")
        openai_key = request.form.get("api_key")
        sapling_key = request.form.get("sapling_key")

        if url and openai_key and sapling_key:
            
            raw_reviews = []
            # URL에 특정 문자열이 있는지 확인하여 분기 처리
            if "gmarket.co.kr" in url:
                print("지마켓 URL 감지됨. 지마켓 크롤러를 실행합니다.")
                raw_reviews = get_gmarket_reviews(url)
            elif "coupang.com" in url:
                print("쿠팡 URL 감지됨. 쿠팡 크롤러를 실행합니다.")
                # 웹 앱에서는 속도를 위해 최대 페이지 수 제한
                raw_reviews = get_coupang_reviews(url, max_pages=3)
            else:
                analysis_result = {"error": "지원하지 않는 URL입니다. 지마켓 또는 쿠팡 URL을 입력해주세요."}

            # raw_reviews가 성공적으로 수집되었을 때만 후속 처리 진행
            if raw_reviews:
                human_reviews = filter_reviews_by_ai(raw_reviews, sapling_key)
                filter_info = f"총 {len(raw_reviews)}개의 리뷰 중 AI 의심 리뷰 {len(raw_reviews) - len(human_reviews)}개를 제외하고 분석했습니다."

                if human_reviews:
                    analysis_result = analyze_reviews_in_one_call(human_reviews, openai_key)
                    reviews = human_reviews
                else:
                    analysis_result = {"summary": "분석할 수 있는 사용자 리뷰가 없습니다. (AI리뷰 필터링 후)"}
            
            # raw_reviews가 비어있고, analysis_result에 에러 메시지가 없을 때
            elif not analysis_result:
                analysis_result = {"error": "리뷰를 가져오지 못했습니다."}

    return render_template("index.html", reviews=reviews, result=analysis_result, filter_info=filter_info)

if __name__ == "__main__":
    app.run(debug=True)