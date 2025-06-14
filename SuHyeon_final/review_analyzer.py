from openai import OpenAI
import json

def analyze_reviews_in_one_call(reviews, api_key):
    """
    한 번의 API 호출로 리뷰 요약, 감정 분석, 신뢰도 점수를 모두 처리합니다.
    결과는 JSON 형식으로 반환받아 파싱합니다.
    """
    try:
        client = OpenAI(api_key=api_key)
        text_to_analyze = "\n".join(reviews[:20])

        prompt = f"""
        다음 한국어 쇼핑몰 리뷰들을 분석해줘.
        분석 결과를 반드시 아래와 같은 JSON 형식으로만 응답해줘. 다른 설명은 붙이지 마.

        {{
          "summary": "리뷰들의 핵심 내용을 1~2 문장으로 요약",
          "sentiment": {{
            "positive_count": "긍정적인 리뷰의 개수 (숫자만)",
            "negative_count": "부정적인 리뷰의 개수 (숫자만)",
            "neutral_count": "중립적인 리뷰의 개수 (숫자만)",
            "overall_analysis": "전반적인 긍정/부정 분위기에 대한 간단한 설명"
          }},
          "trust_score": {{
            "score": "리뷰들의 신뢰도 점수 (0~100 사이의 숫자)",
            "reason": "신뢰도 점수를 그렇게 판단한 이유 (예: 과장된 표현, 구체적인 묘사 등)"
          }}
        }}

        --- 분석할 리뷰 목록 ---
        {text_to_analyze}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"}, 
            messages=[
                {
                    "role": "system",
                    "content": "당신은 한국어 리뷰를 분석하여 지정된 JSON 형식으로 결과를 반환하는 유능한 분석가입니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        result_json = json.loads(response.choices[0].message.content)
        return result_json

    except json.JSONDecodeError:
        return {"error": "모델이 유효한 JSON을 반환하지 않았습니다."}
    except Exception as e:
        return {"error": f"API 호출 중 에러 발생: {e}"}