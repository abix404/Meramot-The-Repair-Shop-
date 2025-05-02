from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Base URL
BASE_URL = "http://127.0.0.1:8000"

image_path = os.path.abspath("media/sellers/saq.jpg")

def test_seller_signup():
    driver.get(f"{BASE_URL}/seller/seller_signup/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("testseller1")
    driver.find_element(By.NAME, "email").send_keys("seller1@example.com")
    driver.find_element(By.NAME, "password1").send_keys("SellerPass123")
    driver.find_element(By.NAME, "password2").send_keys("SellerPass123")
    driver.find_element(By.NAME, "mobile_no").send_keys("0198765432")
    driver.find_element(By.NAME, "address").send_keys("dhaka")
    driver.find_element(By.NAME, "experience").send_keys("1 year")
    driver.find_element(By.ID, "id_image").send_keys(image_path)  # Provide full path
    submit_btn = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click()
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)
    print("✅ Seller sign-up tested (awaiting admin approval).")

def test_seller_login():
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("testseller1")
    driver.find_element(By.NAME, "password").send_keys("SellerPass123")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)
    print("✅ Seller login tested (must be approved first).")

def test_seller_add_product():
    driver.get(f"{BASE_URL}")
    time.sleep(10)
    driver.get(f"{BASE_URL}/seller/seller-dashboard/")
    time.sleep(2)


test_seller_signup()
test_seller_login()
test_seller_add_product()

# Quit driver
driver.quit()