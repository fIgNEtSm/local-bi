from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

url = "https://www.google.com/maps/place/Siri's+Dine+Inn/@18.0104206,79.5498378,16z/data=!4m12!1m2!2m1!1sRestaurants!3m8!1s0x3a334fb3a0490f7d:0xd80c1922d06341af!8m2!3d18.010686!4d79.5591736!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWZhbWlseV9yZXN0YXVyYW50qgFEEAEqDyILcmVzdGF1cmFudHMoADIeEAEiGuInnWVrUEwRITwVosFBOxis3ebJVx8poGpoMg8QAiILcmVzdGF1cmFudHPgAQA!16s%2Fg%2F11v68dv3ww?entry=ttu&g_ep=EgoyMDI1MTExNy4wIKXMDSoASAFQAw%3D%3D"
driver.get(url)
time.sleep(4)

# Try all possible containers
selectors = [
    'div[aria-label="Reviews"]',
    'div[aria-label*="reviews"]',
    'div.m6QErb',
    'div.MyEned',
    'div.fysCi',
    'div[role="main"]',
]

for sel in selectors:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"FOUND → {sel}")
    except:
        print(f"NOT FOUND → {sel}")

driver.quit()
