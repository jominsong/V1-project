import requests
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed

def translate(text):
    try:
        return GoogleTranslator(source='ko', target='en').translate(text)
    except Exception as e:
        print(f"번역 중 오류 발생: {e}")
        return text

def detect_ai_score(text, api_key):
    response = requests.post(
        "https://api.sapling.ai/api/v1/aidetect",
        json={
            "key": api_key,
            "text": text
        }
    )
    result = response.json()
    return round(result["score"] * 100, 2) if "score" in result else None

def process_review(korean_text, api_key):
    try:
        english_text = translate(korean_text)
        score = detect_ai_score(english_text, api_key)
        
        if score is not None and score < 30:
            return korean_text
        return None
    except Exception as e:
        print(f"리뷰 처리 중 오류 발생: {e}")
        return None


def filter_reviews_by_ai(review_list, api_key):
    """
    app.py에서 호출
    리뷰 리스트와 API 키를 받아 AI 리뷰를 걸러내고, 순수 리뷰 리스트를 반환
    """
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_review = {executor.submit(process_review, review, api_key): review for review in review_list}
        for future in as_completed(future_to_review):
            result = future.result()
            if result:
                results.append(result)
    return results
