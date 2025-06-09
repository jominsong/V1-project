from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # UI 없는 환경에서도 실행 가능
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    return driver

def get_reviews(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(2)

    try:
        # 리뷰 탭 클릭
        tabs = driver.find_elements(By.CSS_SELECTOR, '#btfTab > ul > li')
        for tab in tabs:
            if '리뷰' in tab.text or '상품리뷰' in tab.text:
                tab.click()
                break
        time.sleep(2)
    except Exception as e:
        print(f"[오류] 리뷰 탭 클릭 실패: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('article', class_='sdp-review__article__list')
    reviews = []

    for a in articles:
        content_tag = a.find('div', class_='sdp-review__article__list__review__content')
        if content_tag:
            content = content_tag.get_text(strip=True)
            reviews.append(content)

    driver.quit()
    return reviews
