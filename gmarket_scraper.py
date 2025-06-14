from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time
from webdriver_manager.chrome import ChromeDriverManager

def get_gmarket_reviews(url, max_count=10, timeout=10):
    
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    wait = WebDriverWait(driver, timeout)

    reviews = []
    try:
        driver.get(url)

        try:
            review_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"상품평")]')))
            review_tab.click()
        except TimeoutException:
            print("상품평 탭을 찾을 수 없거나 클릭할 수 없습니다.")
            pass
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr td.comment-content p.con")))
        
        review_elements = driver.find_elements(By.CSS_SELECTOR, "tr")
        
        for tr in review_elements:
            try:
                content = tr.find_element(By.CSS_SELECTOR, "td.comment-content p.con").text.strip()
                if content:
                    reviews.append(content)
                    print(f"[{len(reviews)}]:", content)
                    if len(reviews) >= max_count:
                        break
            except NoSuchElementException:
                continue
    
    except TimeoutException:
        print(f"페이지 로딩 시간이 너무 깁니다 (URL: {url})")
    except Exception as e:
        print(f"크롤링 중 알 수 없는 에러 발생: {e}")

    finally:
        driver.quit()
    
    return reviews