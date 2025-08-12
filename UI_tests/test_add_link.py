import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from UI_tests.utils import build_driver

from dotenv import load_dotenv; load_dotenv()


class TestAddLink(unittest.TestCase):
    def setUp(self):
        self.driver = build_driver()

        self.base_url = os.getenv("LINKACE_URL")
        self.email = os.getenv("LINKACE_EMAIL")
        self.password = os.getenv("LINKACE_PASSWORD")
        if not self.email or not self.password:
            raise RuntimeError("Missing LINKACE_EMAIL or LINKACE_PASSWORD env vars")

        self.driver.get(f"{self.base_url}/login")
        self.login_page = LoginPage(self.driver)

    def test_add_and_delete_link(self):
        links_page = self.login_page.login(self.email, self.password)

        links_page.click_quick_add_link()
        url = "https://www.facebook.com/"
        links_page.add_link(url)

        assert links_page.is_link_present("www.facebook.com")
        links_page.go_home()

        links_page.go_to_links()
        links_page.delete_link_from_index("www.facebook.com")
        links_page.clear_trash_links()

        links_page.go_home()
        assert not links_page.is_link_present("www.facebook.com")

    def tearDown(self):
        try:
            self.driver.quit()
        except Exception:
            pass
