from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def crawl_reviews():
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  
  def wait_for_elements(css_selector, driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    elements = wait.until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )
    return elements
  
  url = "https://www.naver.com/"
  driver.get(url)
  wait_for_elements('#search #query', driver)
  
  search_box = driver.find_element(By.CSS_SELECTOR, '#search #query')
  search_box.send_keys('영화')
  search_box.send_keys(Keys.RETURN)
  wait_for_elements('.sc_new .card_area .card_item .data_area .data_box .area_text_box ._text', driver)
  
  review_data_list = []
  
  main_window = driver.current_window_handle
  def collect_reviews_on_page():
    cards = driver.find_elements(By.CSS_SELECTOR, '.sc_new .card_area .card_item .data_area .data_box .area_text_box ._text')
    
    for i, card in enumerate(cards):
      print(f"[{i+1}/{len(cards)}]번 째 영화 크롤링")
      
      ActionChains(driver).key_down(Keys.CONTROL).click(card).key_up(Keys.CONTROL).perform()
      
      driver.switch_to.window(driver.window_handles[-1])
      wait_for_elements('.sc_new .tab_list ._item:nth-of-type(5)', driver)
      
      go_review_btn = driver.find_element(By.CSS_SELECTOR, '.sc_new .tab_list ._item:nth-of-type(5)')
      go_review_btn.click()
      time.sleep(2)
  
      review_box = driver.find_element(By.CSS_SELECTOR, '.lego_review_list')
      driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_box)
      time.sleep(2)
  
      title = driver.find_element(By.CSS_SELECTOR, '.sc_new .title_area .title .area_text_title ._text')
      score = driver.find_elements(By.CSS_SELECTOR, '.lego_review_list .area_card_outer .area_card .area_title_box .area_text_box')
      text = driver.find_elements(By.CSS_SELECTOR, '.lego_review_list .area_card_outer .area_card .area_review_content ._text')
      date = driver.find_elements(By.CSS_SELECTOR, '.lego_review_list .area_card_outer .area_card .cm_upload_info dd:nth-of-type(2)')
      pos = driver.find_elements(By.CSS_SELECTOR, '.lego_review_list .area_card_outer .area_card .cm_sympathy_area ._btn_upvote ._count_num')
      neg = driver.find_elements(By.CSS_SELECTOR, '.lego_review_list .area_card_outer .area_card .cm_sympathy_area ._btn_downvote ._count_num')
  
      for j in range(len(score)):
        review_data = {
          'title': title.text,
          'score': score[j].text,
          'text': text[j].text,
          'date': date[j].text,
          'positive': pos[j].text,
          'negative': neg[j].text
        }
        review_data_list.append(review_data)
  
      driver.close()
      driver.switch_to.window(main_window)
      
  collect_reviews_on_page()
  
  driver.quit()
  return review_data_list