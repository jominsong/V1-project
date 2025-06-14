from flask import Flask, render_template, request, jsonify
from coupang_scraper import get_coupang_reviews
from gmarket_scraper import get_gmarket_reviews
from review_analyzer import analyze_reviews_in_one_call
from ai_detector import filter_reviews_by_ai
import time

app = Flask(__name__)

@app.route("/")
def index():
    """메인 URL 입력 페이지를 보여줍니다."""
    return render_template("index.html")

@app.route("/analyze", methods=['POST'])
def analyze():
    """크롤링 및 분석을 수행하고 결과를 JSON으로 반환합니다."""
    data = request.get_json()
    url = data.get("url")
    openai_key = data.get("openai_key")
    sapling_key = data.get("sapling_key")

    if not all([url, openai_key, sapling_key]):
        return jsonify({"error": "URL, OpenAI 키, Sapling 키가 모두 필요합니다."}), 400

    raw_reviews = []
    if "gmarket.co.kr" in url:
        raw_reviews = get_gmarket_reviews(url)
    elif "coupang.com" in url:
        raw_reviews = get_coupang_reviews(url, max_pages=3)
    else:
        return jsonify({"error": "지원하지 않는 URL입니다. 지마켓 또는 쿠팡 URL을 입력해주세요."}), 400

    if not raw_reviews:
        return jsonify({"error": "리뷰를 가져오지 못했습니다."}), 500

    human_reviews = filter_reviews_by_ai(raw_reviews, sapling_key)
    filter_info = f"총 {len(raw_reviews)}개의 리뷰 중 AI 의심 리뷰 {len(raw_reviews) - len(human_reviews)}개를 제외하고 분석했습니다."

    if not human_reviews:
        return jsonify({"summary": "분석할 수 있는 사용자 리뷰가 없습니다.", "filter_info": filter_info})

    analysis_result = analyze_reviews_in_one_call(human_reviews, openai_key)
    analysis_result['filter_info'] = filter_info
    analysis_result['reviews'] = human_reviews

    return jsonify(analysis_result)

@app.route("/result")
def result():
    """결과 데이터를 받아 result.html 페이지를 렌더링합니다."""
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)