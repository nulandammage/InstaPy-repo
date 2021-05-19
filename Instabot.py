from datetime import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


timenow = datetime.now()
browser = Firefox("./geckodriver")
browser.get("https://www.instagram.com/")
time.sleep(5)
browser.close()
print(datetime.now() - timenow)

