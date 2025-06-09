from bs4 import BeautifulSoup
import requests

def get_reviews(goodscode, max_pages=3, max_reviews=30):
    reviews = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, max_pages + 1):
        url = f"https://diary2.gmarket.co.kr/Review/ViewPremiumReview?goodsCode={goodscode}&type=all&page={page}"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            break
        soup = BeautifulSoup(res.text, "html.parser")
        tags = soup.find_all("p", class_="con")
        for tag in tags:
            text = tag.get_text(strip=True)
            if text:
                reviews.append(text)
            if len(reviews) >= max_reviews:
                return reviews
    return reviews
