from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

options = Options()
options.add_experimental_option("detach", True)
options.add_argument( "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")

path = "C:/Users/PMLS/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s,options=options)
webURL = "https://www.nike.com/au/"

web = driver.get(webURL)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "html.parser")
print(f"webHelloasd",soup.title.text)
time.sleep(3)
input("Press Enter to close the browser...")