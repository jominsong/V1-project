import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_coupang_reviews(url, max_pages=3, timeout=20):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument("window-size=1920x1080")
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = None
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        wait = WebDriverWait(driver, timeout)
        
        all_reviews_text = []
        
        driver.get(url)

        try:
            review_tab_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@name='review']")))
            review_tab_link.click()
            print("상품평 탭(a[@name='review'])을 클릭하여 이동했습니다.")
        except TimeoutException:
            print("상품평 탭을 찾을 수 없어 현재 페이지에서 수집을 시작합니다.")
            pass

        for page_num in range(1, max_pages + 1):
            print(f"--- {page_num} 페이지 리뷰 수집 시작 ---")
            
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.sdp-review__article__list")))
                review_articles = driver.find_elements(By.CSS_SELECTOR, "article.sdp-review__article__list")

                for article in review_articles:
                    try:
                        content = article.find_element(By.CSS_SELECTOR, "div.sdp-review__article__list__review__content").text.strip()
                        if content:
                            all_reviews_text.append(content)
                    except NoSuchElementException:
                        continue
                
                print(f"{page_num} 페이지에서 {len(review_articles)}개의 리뷰를 확인했습니다.")

                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sdp-review__pagination__next-page")))
                
                if not next_button.is_enabled():
                    print("마지막 페이지입니다. 수집을 종료합니다.")
                    break
                
                next_button.click()

            except (TimeoutException, NoSuchElementException):
                print(f"{page_num} 페이지 처리 중 오류 또는 마지막 페이지 도달.")
                break

    except Exception as e:
        print(f"크롤링 프로세스 중 심각한 에러 발생: {e}")
        return []
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    return all_reviews_text