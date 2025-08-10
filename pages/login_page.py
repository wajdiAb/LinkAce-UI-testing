from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from links_page import LinksPage

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.NAME, "email")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        # Wait for login page to load fully
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input)
        )
        assert "Login" in self.driver.title

    def login(self, email, password):
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input)
        )
        email_field.clear()
        email_field.send_keys(email)
        
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        )
        password_field.clear()
        password_field.send_keys(password)
        
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()

        # Optionally wait for post-login redirect here:
        # WebDriverWait(self.driver, 10).until(EC.title_contains("Dashboard"))
        
        return LinksPage(self.driver)
