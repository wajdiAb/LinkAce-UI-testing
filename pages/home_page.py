from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:8080"  # Adjust this if your base URL is different

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        # Wait for dashboard/home page to load after login
        WebDriverWait(self.driver, 10).until(
            lambda d: "Dashboard" in d.title
        )

    def click_quick_add_link(self):
        # Wait for the button to be clickable and click it
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))
        ).click()
        # Wait for the URL field in the modal/form to become visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "url"))
        )
        return self

    def add_link(self, url, title=None):
        url_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "url"))
        )
        url_input.clear()
        url_input.send_keys(url)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form button[type='submit']"))
        ).click()

        # Wait for modal to close (URL input to disappear)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//input[@name='url']"))
        )
        # Optionally, wait for "Quick Add Link" button to be clickable again
        # WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Quick Add Link')]"))
        # )
        return self


    def is_link_present(self, title):
        self.go_home()
        title = title.strip().lower()

        # wait for the Recent Links list
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.link-listing"))
        )

        # find an <a> in Recent Links whose normalized text contains the needle
        xpath = (
            "//ul[contains(@class,'link-listing')]"
            "//a[contains(@class,'list-group-item')][contains("
            "translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
            f"'{title}')]"
        )
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False
        

    def go_home(self):
        """Go to dashboard where 'Recent Links' panel is visible."""
        # Try clicking the brand/logo first
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'navbar-brand') or contains(@class,'logo')]"))
            ).click()
        except Exception:
            self.driver.get(f"{BASE_URL}/")  # fallback

        # Wait for the dashboard marker
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'card-header')][normalize-space()='Recent Links']"))
        )
        return self
    


    def delete_link(self, text):
        """From Home, open the recent link that contains `text`, then delete on details page."""
        # Ensure we’re on home first
        self.go_home()

        # Open the link from 'Recent Links'
        link_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[.//h2[contains(.,'Recent Links')]]//a[contains(normalize-space(), '{text}')]"
                )
            )
        )
        link_el.click()

        # Click Delete on details page (try common variants)
        for xp in [
            "//button[contains(.,'Delete')]",
            "//a[contains(@class,'btn') and contains(.,'Delete')]",
            "//form[.//button[contains(.,'Delete')]]//button[contains(.,'Delete')]",
        ]:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                ).click()
                break
            except Exception:
                continue
        else:
            raise AssertionError("Delete button not found on link details page.")

        # Confirm JS alert if present
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

        # Wait for redirect or success signal
        WebDriverWait(self.driver, 10).until(
            lambda d: "/links" in d.current_url
                      or d.find_elements(By.XPATH, "//*[contains(@class,'alert') and contains(.,'deleted')]")
        )
        return self

    def go_to_trash(self):
        """Click the Trash link in the navbar and wait for the page to load."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Trash']"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Trash')]"))
        )
        return self

    def clear_trash_links(self):
        """
        On the Trash page, click 'Clear Trash' for the 'links' model,
        confirm if prompted, and wait until the section is empty.
        """
        self.go_to_trash()

        # Click the Clear Trash button for the 'links' section
        clear_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//form[contains(@action,'/trash/clear')]"
                "[.//input[@name='model' and @value='links']]"
                "//button[@title='Clear Trash' or contains(.,'Clear Trash')]"
            ))
        )
        clear_btn.click()

        # Accept JS confirm if present
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

        # Wait until the 'Trashed links' card shows it's empty
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'card')][.//div[normalize-space()='Trashed links']]"
                "//*[contains(.,'No entries to be deleted.')]"
            ))
        )
        return self
    
    def go_to_links(self):
        """Navigate to the main Links page and wait for it to load."""
        try:
            # Click the 'Links' navbar item (top-left)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//nav//a[normalize-space()='Links']"))
            ).click()
        except Exception:
            # Fallback: direct navigation
            self.driver.get(f"{BASE_URL}/links")

        # Wait for the Links page header or table to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//h3[normalize-space()='Links'] | //div[contains(@class,'card-header')][normalize-space()='All Links']"
            ))
        )
        return self

    def delete_link_from_index(self, text):
        """Delete a link from the index page by its text."""
        self.go_to_links()

        # Find the link in the index table
        link_row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//div[contains(@class, 'link-wrapper')][contains(., '{text}')]"
            ))
        )

        # Click the delete button in that row
        delete_btn = link_row.find_element(By.XPATH, ".//button[contains(@class,'btn-danger') or contains(.,'Delete')]")
        delete_btn.click()

        # Confirm JS alert if present
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

        # Wait for the deletion to be confirmed (e.g., success message)
        WebDriverWait(self.driver, 10).until(
            lambda d: not d.find_elements(By.XPATH, f"//table//td[contains(., '{text}')]")
        )
        return self