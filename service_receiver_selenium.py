from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Base URL
BASE_URL = "http://127.0.0.1:8000"

def test_user_signup():
    driver.get(f"{BASE_URL}/signup/")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    time.sleep(0.5)
    driver.find_element(By.NAME, "email").send_keys("testuser1@gmail.com")
    time.sleep(0.5)
    driver.find_element(By.NAME, "mobile_no").send_keys("0123456789")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password1").send_keys("TestPass123")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password2").send_keys("TestPass123")
    time.sleep(0.5)
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
    checkbox.click()
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)
    print("✅ User sign-up tested.")

def test_user_login():
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    time.sleep(0.5)
    driver.find_element(By.NAME, "password").send_keys("TestPass123")
    time.sleep(1)
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(0.5)
    button.click()
    print("✅ User login tested.")

def test_user_home():
    driver.get(f"{BASE_URL}")
    time.sleep(5)
    print("Current URL:", driver.current_url)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "query"))
    )
    search_box.send_keys("AC")
    time.sleep(3)
    search_box.send_keys(Keys.RETURN)
    print("✅ Search submitted for: AC")
    time.sleep(2)

    view_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "View Details"))
    )
    view_button.click()
    time.sleep(2)

    driver.find_element(By.LINK_TEXT, "Book Now").click()
    time.sleep(2)

    driver.find_element(By.NAME, "date").send_keys("05-10-2025")
    time.sleep(0.5)
    driver.find_element(By.NAME, "time_slot").send_keys("11:00 AM - 12:00 PM")

    button = driver.find_element(By.XPATH, "//button[text()='Confirm Booking']")
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(0.5)
    button.click()
    time.sleep(3)

# 4. Logout
def test_user_logout():
    driver.get(f"{BASE_URL}/logout/")
    print("👋 Logged out.")


# Run all tests
test_user_signup()
test_user_login()
test_user_home()
test_user_logout()

# Quit driver
driver.quit()