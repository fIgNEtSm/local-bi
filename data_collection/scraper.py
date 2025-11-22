from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, random

# Human-like random sleep
def human_sleep(a=1.0, b=2.0):
    time.sleep(random.uniform(a, b))

# Detect correct scroll container
def get_scroll_container(driver):
    selectors = [
        'div[aria-label*="reviews"]',
        'div.m6QErb',
        'div.MyEned'
    ]
    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            print("Using scroll container:", sel)
            return el
        except:
            continue
    raise Exception("No valid scroll container found")

def scrape_google_reviews(url, max_scrolls=50):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    human_sleep(3,4)

    scroll_div = get_scroll_container(driver)
    actions = ActionChains(driver)
    actions.move_to_element(scroll_div).perform()
    human_sleep(1,2)

    # Scroll loop to load more reviews
    last_height = -1
    for i in range(max_scrolls):
        driver.execute_script("arguments[0].scrollBy(0, 400);", scroll_div)
        human_sleep(0.8, 1.5)

        new_height = driver.execute_script("return arguments[0].scrollTop;", scroll_div)
        if new_height == last_height:
            print("Reached bottom or no more new reviews.")
            break
        last_height = new_height

    # Extract reviews
    review_elements = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
    print("Found review blocks:", len(review_elements))

    reviews = []
    for r in review_elements:
        author = rating = text = date = None

        try:
            author = r.find_element(By.CSS_SELECTOR, "span.X43Kjb").text
        except: pass
        try:
            rating = r.find_element(By.CSS_SELECTOR, "span.kvMYJc").get_attribute("aria-label")
        except: pass
        try:
            text = r.find_element(By.CSS_SELECTOR, "span.wiI7pd").text
        except: pass
        try:
            date = r.find_element(By.CSS_SELECTOR, "span.duhH3b").text
        except: pass

        if author or rating or text:
            reviews.append({
                "author": author,
                "rating": rating,
                "text": text,
                "date": date
            })

    driver.quit()
    return reviews

url = "https://www.google.com/maps/place/Siri's+Dine+Inn/@18.0104206,79.5498378,16z/data=!4m12!1m2!2m1!1sRestaurants!3m8!1s0x3a334fb3a0490f7d:0xd80c1922d06341af!8m2!3d18.010686!4d79.5591736!9m1!1b1!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBEWZhbWlseV9yZXN0YXVyYW50qgFEEAEqDyILcmVzdGF1cmFudHMoADIeEAEiGuInnWVrUEwRITwVosFBOxis3ebJVx8poGpoMg8QAiILcmVzdGF1cmFudHPgAQA!16s%2Fg%2F11v68dv3ww?entry=ttu&g_ep=EgoyMDI1MTExNy4wIKXMDSoASAFQAw%3D%3D"  # put your "See All Reviews" link
reviews = scrape_google_reviews(url)
print(reviews)  # output 
