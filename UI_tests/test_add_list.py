import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")   # this option is also needed sometimes when running in CI. It disables security features of Chrome

driver = webdriver.Chrome(options=options)

class TestAddList(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:80/login")
        self.driver.maximize_window()

    def test_add_list(self):
        driver = self.driver

        # Login
        driver.find_element(By.NAME, "email").send_keys("wagde.abo164@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("Wajdi0355", Keys.RETURN)

        # Wait for dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/links']"))
        )

        # Navigate to Lists page
        driver.get("http://localhost:80/lists")

        # Click "Add List" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/lists/create']"))
        ).click()

        # Fill list form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        ).send_keys("My Test List")

        driver.find_element(By.NAME, "description").send_keys("This is a Selenium-created list.")

        # Submit form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Assert list appears in list table
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        self.assertIn("created", success_message.text.lower())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
