from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

options = Options()
options.add_experimental_option("detach", True)
# Fake User-Agent
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
)
path = "C:/Users/PMLS/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s, options=options)

all_data = []

# apna starting page ka URL yahan dal do
url = "https://www.daraz.pk/catalog/?q=hoodies%20sweatshirts"
driver.get(url)

while True:
    # wait until products list load ho jaye
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.RfADt a"))
    )

    # ab page ka soup lo
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # titles, prices, ratings scrape karo
    title = [a.get_text(strip=True) for a in soup.select("div.RfADt a")]
    price = [p.get_text(strip=True) for p in soup.find_all("span", class_="ooOxS")]
    rate = [r.get_text(strip=True) for r in soup.find_all("span", class_="oa6ri")]

    for t, p, r in zip(title, price, rate):
        all_data.append([t, p, r])

    print(f"✅ Page scraped: {len(title)} items. Total so far: {len(all_data)}")

    time.sleep(2)  # thoda wait to mimic human

    # Next button check karo
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next")
        # agar disabled hai -> last page
        if "ant-pagination-disabled" in next_button.get_attribute("class"):
            print("🚨 Last page reached.")
            break
        else:
            driver.execute_script("arguments[0].click();", next_button)  # JS click (zyada reliable hota hai)
    except Exception as e:
        print("⚠️ Next button not found, stopping.")
        break

# save to CSV
df = pd.DataFrame(all_data, columns=["Title", "Price", "Rating"])
df.to_csv("daraz_products.csv", index=False, encoding="utf-8-sig")
print("🎉 Scraping Completed. Data saved to daraz_products.csv")
