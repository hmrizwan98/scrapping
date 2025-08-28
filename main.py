from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# ====== CONFIG ======
proxy = "67.43.236.19:3527"   # Optional proxy (remove if not working)
email = "rizwan+dev@expedey.com"     # apna LinkedIn email likho
password = "Hello123@"  # apna LinkedIn password likho
chromedriver_path = r"C:/Users/PMLS/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
# ====================

# Chrome Options
options = Options()
options.add_experimental_option("detach", True)
# options.add_argument(f'--proxy-server=http://{proxy}')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)

# Start Driver
s = Service(chromedriver_path)
driver = webdriver.Chrome(service=s, options=options)

# Open LinkedIn Login
driver.get("https://www.linkedin.com/login")

try:
    # Wait for Email field & Enter Email
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(email)

    # Enter Password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Press ENTER (instead of clicking login button)
    password_field.send_keys(Keys.RETURN)

    # Wait for Feed page after login
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "global-nav-search"))  # navbar element
    )
    print("✅ Login successful!")

    # Page Scroll (load more posts)
    height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == height:
            break
        height = new_height

    # Extract Images
    imgs = driver.find_elements(By.CSS_SELECTOR, "img.ivm-view-attr__img--centered.update-components-actor__avatar-image")
    img_urls = [i.get_attribute("src") for i in imgs]

    # Extract Titles (names)
    titles = driver.find_elements(By.CSS_SELECTOR, ".update-components-actor__single-line-truncate span")
    title_texts = [t.text.strip() for t in titles if t.text.strip() != ""]

    # Extract Descriptions (headlines)
    descs = driver.find_elements(By.CSS_SELECTOR, "span.update-components-actor__description.text-body-xsmall")
    desc_texts = [d.text.strip() for d in descs if d.text.strip() != ""]

    # ✅ Equalize lengths (fill with "-")
    max_len = max(len(img_urls), len(title_texts), len(desc_texts))

    def pad_list(lst, length):
        return lst + ["-"] * (length - len(lst))

    img_urls = pad_list(img_urls, max_len)
    title_texts = pad_list(title_texts, max_len)
    desc_texts = pad_list(desc_texts, max_len)

    # Save into DataFrame
    data = pd.DataFrame({
        "Image": img_urls,
        "Title": title_texts,
        "Description": desc_texts
    })

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    print(data)
    data.to_csv("data/linkedin_scraped.csv", index=False, encoding="utf-8-sig")
    print("✅ Data saved to linkedin_scraped.csv")

except Exception as e:
    print("❌ Error:", e)

# Optional: Wait before closing
time.sleep(5)
