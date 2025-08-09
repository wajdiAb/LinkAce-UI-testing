from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")   # this option is also needed sometimes when running in CI. It disables security features of Chrome

driver = webdriver.Chrome(options=options)

# def test_login():
#     driver = webdriver.Chrome()
#     driver.get("http://localhost:80/login")

#     # Fill in login form
#     username_input = driver.find_element(By.NAME, "email")
#     password_input = driver.find_element(By.NAME, "password")
#     username_input.send_keys("wagde.abo164@gmail.com")  # <--- Change this
#     password_input.send_keys("Wajdi0355")  # <--- Change this
#     password_input.send_keys(Keys.RETURN)

#     # Wait for dashboard to load (adjust selector if needed)
#     try:
#         dashboard_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard, .main-header, .navbar, .sidebar"))
#         )
#         print("Dashboard element found!")
#     except Exception as e:
#         print("Dashboard did not load, page title is:", driver.title)
#         driver.quit()
#         assert False, f"Dashboard did not load after login: {e}"

#     assert "Dashboard" in driver.title or "LinkAce" in driver.title
#     driver.quit()

# def test_add_link():
#     driver = webdriver.Chrome()
#     driver.get("http://localhost:80/login")
#     driver.find_element(By.NAME, "email").send_keys("wagde.abo164@gmail.com")
#     driver.find_element(By.NAME, "password").send_keys("Wajdi0355", Keys.RETURN)

#     # Wait for login
#     WebDriverWait(driver, 10).until(lambda d: d.title != "Login - LinkAce")

#     # Wait for and click the "Quick Add Link" button
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-primary"))
#     )
#     buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn-primary")
#     for btn in buttons:
#         if "Quick Add Link" in btn.text:
#             btn.click()
#             break

#     # (Continue the rest of your test, e.g., fill the form...)

#     driver.quit()

def test_add_link():
    driver = webdriver.Chrome()
    driver.get("http://localhost:80/login")
    driver.find_element(By.NAME, "email").send_keys("wagde.abo164@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Wajdi0355", Keys.RETURN)

    # Wait for login to finish (dashboard or any post-login indicator)
    WebDriverWait(driver, 10).until(lambda d: d.title != "Login - LinkAce")

    # Click "Quick Add Link"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-primary"))
    )
    quick_add_clicked = False
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn-primary")
    for btn in buttons:
        if "Quick Add Link" in btn.text:
            btn.click()
            quick_add_clicked = True
            break
    assert quick_add_clicked, "Could not find 'Quick Add Link' button."

    # Fill URL field (wait for it to be visible)
    url = "https://www.wikipedia1.org"
    url_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "url"))
    )
    url_field.send_keys(url)

    # Click the visible Add/Save button
    time.sleep(0.5)  # Sometimes needed for button to enable
    submit_clicked = False
    btns = driver.find_elements(By.CSS_SELECTOR, "button.btn-primary")
    for btn in btns:
        if btn.is_displayed() and ("Add" in btn.text or "Save" in btn.text or "Create" in btn.text):
            btn.click()
            submit_clicked = True
            break
    assert submit_clicked, "Could not find and click the submit button after entering URL."

    # Wait for the new link to show up by anchor href
    time.sleep(1.5)  # Wait for new link to appear (adjust if needed)

    print("\n--- DEBUG: Anchors after adding link ---")
    anchors = driver.find_elements(By.TAG_NAME, "a")
    found = False
    for a in anchors:
        href = a.get_attribute("href")
        print(f"ANCHOR: '{a.text}' | HREF: '{href}'")
        if href and url in href:
            found = True
    print("--- END DEBUG ---\n")

    assert found, f"Did not find anchor with href containing {url} after adding link."

    driver.quit()