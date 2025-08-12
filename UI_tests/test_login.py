import os
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from .utils import build_driver

from dotenv import load_dotenv; load_dotenv()



class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = build_driver()
        self.base_url = os.getenv("LINKACE_URL")
        self.email = os.getenv("LINKACE_EMAIL")
        self.password = os.getenv("LINKACE_PASSWORD")
        if not all([self.base_url, self.email, self.password]):
            raise RuntimeError(
                "Missing LINKACE_URL, LINKACE_EMAIL, or LINKACE_PASSWORD env vars"
            )

    def tearDown(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def test_login_success(self):
        self.driver.get(f"{self.base_url}/login")
        login_page = LoginPage(self.driver)
        login_page.login(self.email, self.password)
        self.assertNotIn("Login", self.driver.title)

    def test_login_failure(self):
        self.driver.get(f"{self.base_url}/login")
        # Enter correct email but wrong password
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # An alert should appear and page should stay on login
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        )
        self.assertIn("Login", self.driver.title)