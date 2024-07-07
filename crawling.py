from selenium import webdriver  # 셀레니움을 활성화
from selenium.webdriver.chrome.options import Options

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://mabi.tar.to/")