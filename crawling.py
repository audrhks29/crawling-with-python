from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://mabi.tar.to/")


act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정

# 닉네임 입력
act_input_nickName = driver.find_element(By.CSS_SELECTOR, '#loginForm > input').send_keys('마비굿잡') 

# 확인버튼 클릭
act_click_search = driver.find_element(By.CSS_SELECTOR, '#loginForm > button').click()

# 광고 요소 제거
ad_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="google_ads"], .adsbygoogle, .ad-container')

for ad_element in ad_elements:
  driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", ad_element)

# 스킬 탭 클릭(카테고리 선택)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#container2 > div:nth-child(6) > div:nth-child(3) > div:nth-child(1) > a'))).click()

# 랭크 선택
skills=driver.find_elements(By.CSS_SELECTOR, '.skill')

skills_data = []
skills_index=0

for skill in skills:
  skill_rank = skill.find_element(By.CSS_SELECTOR, '.skill_data')
  skill_effect= skill.find_element(By.CSS_SELECTOR, '.icon').click()
  
  # 랭크 길이
  skill_rank_option = skill.find_elements(By.CSS_SELECTOR, 'option')
  skill_rank_option_length=len(skill_rank_option)
  
  for rank_value in range(0, skill_rank_option_length):
    select_element = Select(skill_rank)
    select_element.select_by_value(str(rank_value))

    skill_data = {
        "name": skill.find_element(By.CSS_SELECTOR, "td.kname").text.strip(),
        "rank": select_element.first_selected_option.text.strip(), 
        "ap": skill.find_element(By.CSS_SELECTOR, "td.AP").text.strip(),
        "hp": skill.find_element(By.CSS_SELECTOR, "td.hp").text.strip(),
        "mp": skill.find_element(By.CSS_SELECTOR, "td.mp").text.strip(),
        "sp": skill.find_element(By.CSS_SELECTOR, "td.sp").text.strip(),
        "str": skill.find_element(By.CSS_SELECTOR, "td.str").text.strip(),
        "dex": skill.find_element(By.CSS_SELECTOR, "td.dex").text.strip(),
        "int": skill.find_element(By.CSS_SELECTOR, "td.int").text.strip(),
        "will": skill.find_element(By.CSS_SELECTOR, "td.will").text.strip(),
        "luck": skill.find_element(By.CSS_SELECTOR, "td.luck").text.strip(),
        "rp":skill.find_element(By.XPATH, "td[13]").text.strip(),
    }
    
    skills_data.append(skill_data)
      
  try:
    # iframe으로 전환
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#pageslide > iframe"))
    )
    driver.switch_to.frame(iframe)

    for table_id in range(0,skill_rank_option_length):
      try:
        table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, str(table_id)))
        )
        effect = table_element.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(3) > td')
        html_content = effect.get_attribute('innerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')
        lines = [line.strip() for line in soup.stripped_strings if line.strip()]
      
        skills_data[skills_index]['effect'] = lines
        skills_index += 1
          
      except Exception as e:
        print(f"Table ID {table_id} not found or error occurred: {e}")
      
  finally:
    driver.switch_to.default_content()
    
# print(skills_data)
# for s in skills_data:
#   print(s)

# 수집한 데이터를 데이터 프레임으로 변환
df = pd.DataFrame(skills_data)

# 엑셀 파일로 저장
df.to_excel("skills_data.xlsx", index=False)