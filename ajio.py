from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
url = "https://www.ajio.com/men-caps-hats/c/830202001"

driver.get(url)
time.sleep(3)

# Scroll till end
height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == height:
        break
    height = new_height

time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")

title_price_rating = []

names = soup.find_all("div", class_="nameCls")
prices = soup.find_all("span", class_="price")
ratings = soup.find_all("p", class_="_3I65V")  # 👈 check if this is correct class

for name, price_tag, rating_tag in zip(names, prices, ratings):
    # Product Name
    product_name = name.get("aria-label", "").strip()

    # Product Price
    strong_tag = price_tag.find("strong")
    product_price = strong_tag.get_text(strip=True) if strong_tag else "N/A"

    # Product Rating
    product_rating = rating_tag.text.strip() if rating_tag else "N/A"

    # Save tuple
    title_price_rating.append((product_name, product_price, product_rating))

pd.DataFrame(title_price_rating, columns=["Product Name", "Price", "Rating"]).to_csv("ajio_caps.csv", index=False)
print(title_price_rating)

# 👇 Keeps browser open until you press Enter
input("Press Enter to close browser...")
driver.quit()
