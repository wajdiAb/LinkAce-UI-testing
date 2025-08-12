# UI_tests/test_add_list.py
import os
import uuid
import unittest


from pages.login_page import LoginPage   # reuse your existing POM
from pages.lists_page import ListsPage
from dotenv import load_dotenv; load_dotenv()
from UI_tests.utils import build_driver
from pages.lists_page import ListsPage




class TestAddList(unittest.TestCase):
    def setUp(self):
        self.driver = build_driver()

        self.base_url = os.getenv("LINKACE_URL")
        self.email = os.getenv("LINKACE_EMAIL")
        self.password = os.getenv("LINKACE_PASSWORD")
        if not self.email or not self.password:
            raise RuntimeError("Missing LINKACE_EMAIL or LINKACE_PASSWORD env vars")
        
        self.driver.get(f"{self.base_url}/login")
        self.login_page = LoginPage(self.driver)
        self.login_page.login(self.email, self.password)


    def tearDown(self):
        self.driver.quit()

    def test_add_list(self):
        lists_page = ListsPage(self.driver)
        list_name = f"UI List {uuid.uuid4().hex[:6]}"
        lists_page.add_list(list_name, description="Created by automated UI test.")
        assert lists_page.is_list_present(list_name), f"List '{list_name}' was not found after creation."

        # Clean up: delete the list
        lists_page.delete_list(list_name)
        assert not lists_page.is_list_present(list_name), f"List '{list_name}' was not deleted successfully."

if __name__ == "__main__":
    unittest.main()
