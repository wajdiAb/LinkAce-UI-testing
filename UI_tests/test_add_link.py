import unittest
from selenium import webdriver
from login_page import LoginPage
from links_page import LinksPage

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")   # this option is also needed sometimes when running in CI. It disables security features of Chrome

driver = webdriver.Chrome(options=options)

class TestAddLink(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://localhost:80/login")
        self.login_page = LoginPage(self.driver)

    # def test_add_link(self):
    #     links_page = self.login_page.login("wagde.abo164@gmail.com", "password")
    #     links_page.click_quick_add_link()
    #     url = "https://www.facebook.com/"
    #     links_page.add_link(url)
    #     # Now check by URL or title (if your app shows the URL/title in the Recent Links)
    #     assert links_page.is_link_present("www.facebook.com")  # or whatever is shown

    def test_add_and_delete_link(self):
        links_page = self.login_page.login("wagde.abo164@gmail.com", "password")

        links_page.click_quick_add_link()
        links_page.add_link("https://www.facebook.com/")

        assert links_page.is_link_present("www.facebook.com")
        links_page.go_home()
        

        # however you delete it (index/details), then:
        links_page.go_to_links()
        # click the per-item Delete on /links (your existing delete)
        links_page.delete_link_from_index("www.facebook.com")  # or whatever you named it

        # finally, clean the trash
        links_page.clear_trash_links()

        # and verify it no longer appears on Home
        links_page.go_home()
        assert not links_page.is_link_present("www.facebook.com")

    



    def tearDown(self):
        self.driver.quit()
