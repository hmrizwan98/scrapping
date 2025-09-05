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

path = "C:/Users/Muhammad Rizwan/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
s = Service(path)
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://www.linkedin.com/login")