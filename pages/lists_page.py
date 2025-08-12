from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
import os

LOWER = "translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"

class ListsPage:
    """POM for creating, finding, and deleting Lists in LinkAce."""

    def __init__(self, driver, base_url: str | None = None):
        self.driver = driver
        self.base_url = (base_url or os.getenv("LINKACE_URL") or "").rstrip("/")
        # When logged in, the global navbar "Add List" exists:
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href$='/lists/create']"))
        )
        self.home_page = HomePage(self.driver)

    # ---------- Navigation ----------
    def open_index(self):
        """Go to /lists (card grid)."""
        url = f"{self.base_url}/lists" if self.base_url else "/lists"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".list-listing")),
                EC.url_contains("/lists")
            )
        )
        return self

    # ---------- Helpers ----------
    def _click_add(self):
        # Works from anywhere (navbar or the page header toolbar)
        add_x = (
            "//a[contains(@href,'/lists/create')]"
            " | //header//a[contains(@href,'/lists/create')]"
            " | //header//button[contains(" + LOWER + ", 'add')]"
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, add_x))
        ).click()

    def _card_xpath_by_name(self, name: str) -> str:
        """Card that contains the list name (case-insensitive) inside the grid."""
        ln = name.lower()
        return (
            f"//div[contains(@class,'list-listing')]"
            f"//div[contains(@class,'card')][.//a[contains({LOWER}, '{ln}')]]"
        )

    # ---------- Create ----------
    def add_list(self, name: str, description: str = ""):
        """Create a new list."""
        self._click_add()

        name_el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        name_el.clear()
        name_el.send_keys(name)

        if description:
            try:
                desc_el = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.NAME, "description"))
                )
                desc_el.clear()
                desc_el.send_keys(description)
            except Exception:
                pass  # description may not exist in some themes

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()

        # Success: flash or redirect to show page
        WebDriverWait(self.driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                EC.url_matches(r".*/lists/\d+.*"),
            )
        )
        return self

    # ---------- Read (checks) ----------
    def is_list_present(self, name: str) -> bool:
        """Check on /lists grid (recommended for your UI)."""
        self.open_index()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._card_xpath_by_name(name)))
            )
            return True
        except Exception:
            return False

    def is_list_present_on_dashboard(self, name: str) -> bool:
        """Alternative: check Dashboard 'Recent Lists' widget."""
        self.home_page.go_home()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"(//div[.//h3[contains({LOWER}, 'recent lists')] "
                    f"   or .//div[contains(@class,'card-header') and contains({LOWER}, 'recent lists')]])"
                    f"//a[contains(@class,'single-list')][contains({LOWER}, '{name.lower()}')]"
                ))
            )
            return True
        except Exception:
            return False

    # ---------- Delete ----------
    def delete_list(self, name: str):
        """Delete a list from the /lists card grid."""
        self.open_index()
        card_x = self._card_xpath_by_name(name)
        card = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, card_x))
        )

        # Try Delete link/button inside the card
        clicked = False
        for xp in [
            ".//a[contains(" + LOWER + ", 'delete')]",
            ".//button[contains(" + LOWER + ", 'delete')]",
        ]:
            try:
                btn = card.find_element(By.XPATH, xp)
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(btn)).click()
                clicked = True
                break
            except Exception:
                continue
        if not clicked:
            raise AssertionError("Delete control not found in the list card")

        # Confirm via alert or modal (depending on build)
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception:
            try:
                modal = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal.show"))
                )
                confirm = modal.find_element(
                    By.XPATH, ".//button[contains(" + LOWER + ", 'delete') or contains(" + LOWER + ", 'confirm')]"
                )
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(confirm)).click()
            except Exception:
                pass  # some setups delete immediately

        # Wait until the card disappears
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, card_x))
        )
        return self























# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.home_page import HomePage

# class ListsPage:
#     """Page object representing the lists index page."""

#     def __init__(self, driver):
#         self.driver = driver
#         # Ensure the lists page has loaded by waiting for the "Add List" button
#         WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/lists/create']"))
#         )
#         self.home_page = HomePage(self.driver)

#     def add_list(self, name, description=""):
#         """Create a new list with the given name and description."""
#         WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/lists/create']"))
#         ).click()

#         WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.NAME, "name"))
#         ).send_keys(name)

#         if description:
#             self.driver.find_element(By.NAME, "description").send_keys(description)

#         self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#         # Wait for success alert indicating creation
#         WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
#         )
#         return self

#     def is_list_present(self, name):
#         self.home_page.go_home()
#         """Return True if a list with the given name exists in the table."""
#         try:
#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, f"//table//a[normalize-space()='{name}']")
#                 )
#             )
#             return True
#         except Exception:
#             return False

#     def delete_list(self, name):
#         """Delete the list with the provided name and wait until it disappears."""
#         row = WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, f"//tr[.//a[normalize-space()='{name}']]") )
#         )

#         # Attempt to click a delete control within the row
#         for xp in [
#             ".//button[contains(@class,'btn-danger') or contains(.,'Delete')]",
#             ".//a[contains(@class,'btn-danger') or contains(.,'Delete')]",
#         ]:
#             try:
#                 row.find_element(By.XPATH, xp).click()
#                 break
#             except Exception:
#                 continue
#         else:
#             raise AssertionError("Delete control not found for list")

#         # Accept confirmation alert if it appears
#         try:
#             WebDriverWait(self.driver, 2).until(EC.alert_is_present())
#             self.driver.switch_to.alert.accept()
#         except Exception:
#             pass

#         WebDriverWait(self.driver, 10).until(
#             EC.invisibility_of_element_located((By.XPATH, f"//tr[.//a[normalize-space()='{name}']]") )
#         )
#         return self