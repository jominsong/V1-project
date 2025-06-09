import os
from openai import OpenAI
from collections import Counter

def summarize_reviews_openai(reviews, api_key):
    try:
        client = OpenAI(api_key=api_key)
        text = "\n".join(reviews[:20])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 한국어 리뷰를 요약해주는 도우미입니다."
                },
                {
                    "role": "user",
                    "content": f"다음 리뷰들을 요약해줘:\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[요약 실패] 에러: {e}"

def analyze_sentiment_openai(reviews, api_key):
    try:
        client = OpenAI(api_key=api_key)
        text = "\n".join(reviews[:20])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 한국어 상품 리뷰의 감정을 분석하는 도우미입니다. 각 리뷰가 긍정적인지 부정적인지 판단하세요."
                },
                {
                    "role": "user",
                    "content": f"다음 리뷰들을 감성 분석해줘. 긍정/부정으로 분류해서 개수를 세줘 전체적인 분석도 첨가해줘:\n{text}"
                }
            ],
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return {"에러": str(e)}
