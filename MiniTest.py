from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service('C:/Users/amina/Documents/ChromeDriver/chromedriver.exe')
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)
driver.get("http://www.google.com")
print(driver.title)
driver.quit()
