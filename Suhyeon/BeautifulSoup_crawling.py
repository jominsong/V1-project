import requests
from bs4 import BeautifulSoup
import re

def get_reviews(goodscode, max_reviews=20):
    """
    G마켓 상품 코드(goodscode)를 기반으로 최대 max_reviews개의 리뷰를 수집
    """
    detail_url = f"https://item.gmarket.co.kr/Item?goodscode={goodscode}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(detail_url, headers=headers)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    # 리뷰 고유 ID(prvw_no) 추출
    prvw_ids = []
    for a in soup.select('a.uxelayer_ctrl'):
        url = a.get('data-pop-layer-url', '')
        m = re.search(r'prvw_no=(\d+)', url)
        if m:
            prvw_ids.append(m.group(1))
    prvw_ids = list(dict.fromkeys(prvw_ids))  # 중복 제거

    reviews = []
    for prvw_no in prvw_ids[:max_reviews]:
        popup_url = f"https://diary2.gmarket.co.kr/Review/ViewPremiumReviewLayer?flag=v&prvw_no={prvw_no}"
        r = requests.get(popup_url, headers=headers)
        if r.status_code != 200:
            continue
        p_soup = BeautifulSoup(r.text, "html.parser")
        con = p_soup.find("p", class_="con")
        if con and (text := con.get_text(strip=True)):
            reviews.append(text)

    return reviews
