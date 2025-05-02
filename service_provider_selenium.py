from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    time.sleep(0.5)
    driver.find_element(By.NAME, "email").send_keys("seller1@gmail.com")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password1").send_keys("SellerPass1234")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password2").send_keys("SellerPass1234")
    time.sleep(0.5)
    driver.find_element(By.NAME, "mobile_no").send_keys("0198765432")
    time.sleep(0.5)
    driver.find_element(By.NAME, "address").send_keys("dhaka")
    time.sleep(0.5)
    driver.find_element(By.NAME, "experience").send_keys("1 year")
    time.sleep(1)
    driver.find_element(By.ID, "id_image").send_keys(image_path)
    time.sleep(0.5)
    button = driver.find_element(By.XPATH, "//button[text()='Sign Up']")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(1)
    button.click()
    time.sleep(2)
    print("✅ Seller sign-up tested.")

def test_seller_login():
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("testseller1")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password").send_keys("SellerPass1234")
    time.sleep(1)
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(0.5)
    button.click()
    print("✅ Seller login tested.")

def test_seller_add_product():
    driver.get(f"{BASE_URL}")
    time.sleep(2)
    print("Current URL:", driver.current_url)
    driver.get(f"{BASE_URL}/seller/seller-dashboard/")
    time.sleep(2)



test_seller_signup()
test_seller_login()
test_seller_add_product()

# Quit driver
driver.quit()