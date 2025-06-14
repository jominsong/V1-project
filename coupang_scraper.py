import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_coupang_reviews(url, max_pages=3, timeout=20):
    """
    undetected-chromedriver를 이용해 쿠팡 리뷰를 크롤링하는 최종 함수.
    - 페이지네이션(페이지 넘김) 및 안정적인 종료 로직 포함
    """
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument("window-size=1920x1080")
    options.add_argument('--disable-blink-features=AutomationControlled')

    # driver 변수를 try 블록 이전에 초기화
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
        # 함수가 리뷰를 반환하기 전에 에러가 나면 빈 리스트를 반환
        return []
    finally:
        # [가장 중요한 부분] 드라이버가 성공적으로 생성되었을 때만 종료를 시도
        if driver:
            try:
                driver.quit()
            except Exception:
                # 종료 시 발생하는 모든 오류를 무시하고 조용히 넘어감
                pass

    return all_reviews_text

# 이 파일을 직접 실행해서 테스트할 때 사용
if __name__ == "__main__":
    # 테스트할 쿠팡 URL
    test_url = "https://www.coupang.com/vp/products/7987262322?itemId=22189207615&vendorItemId=89235434736"
    
    print("="*50)
    print("--- 쿠팡 리뷰 크롤러 단독 테스트 시작 ---")
    
    # 함수 실행 (테스트를 위해 최대 2페이지만 수집)
    reviews = get_coupang_reviews(test_url, max_pages=2)
    
    print("\n" + "="*50)
    print(f"--- 테스트 종료: 총 {len(reviews)}개의 리뷰 수집 완료 ---")

    # 수집된 리뷰 5개만 샘플로 출력
    for i, review_text in enumerate(reviews[:5]):
        print(f"리뷰 {i+1}: {review_text[:100]}...")