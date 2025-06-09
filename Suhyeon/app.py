import streamlit as st
from review_analyzer import summarize_reviews_openai, analyze_sentiment_openai
from BeautifulSoup_crawling import get_reviews

st.set_page_config(page_title="리뷰 요약 및 감성 분석기", layout="centered")

st.title("🛍️ 리뷰 요약 및 감성 분석기( G마켓 )")

api_key = st.text_input("🔑 OpenAI API 키를 입력하세요", type="password")

goodscode = st.text_input("📦 상품 코드를 입력하세요")

if st.button("리뷰 가져오기 및 분석 시작"):
    if not api_key:
        st.error("API 키를 입력해주세요.")
    elif not goodscode:
        st.error("상품 URL을 입력해주세요.")
    else:
        with st.spinner("리뷰를 가져오는 중..."):
            reviews = get_reviews(goodscode)

        if not reviews:
            st.warning("리뷰를 가져오지 못했습니다. 코드가 올바른지 확인해주세요.")
        else:
            st.success(f"{len(reviews)}개의 리뷰를 가져왔습니다.")

            with st.spinner("요약 및 감성 분석 중입니다..."):
                summary = summarize_reviews_openai(reviews, api_key)
                sentiment = analyze_sentiment_openai(reviews, api_key)

            st.subheader("📝 리뷰 요약")
            st.write(summary)

            st.subheader("💬 분석 결과")
            st.json(sentiment)
