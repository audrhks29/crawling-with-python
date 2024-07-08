from selenium import webdriver  # 셀레니움을 활성화
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains  # 액션체인 활성화
from selenium.webdriver.common.by import By
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

# 스킬 탭 클릭
act_click_tab = driver.find_element(By.CSS_SELECTOR, '#container2 > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > a').click()

# 랭크 선택
# act_select_rank = driver.find_element(By.CSS_SELECTOR, '#data_\<\?php\/\/ > option:nth-child(1)').click()


skill_ap = driver.find_elements(By.CSS_SELECTOR, "#CommerceMastery > td.AP")
for i in skill_ap:
    title = i.text
    print(title)
