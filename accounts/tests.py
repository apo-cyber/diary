from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestHomePage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Safari()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        login_url = self.live_server_url + reverse_lazy('account_login')
        self.selenium.get(login_url)

        username_input = self.selenium.find_element(By.NAME, 'login')
        username_input.send_keys('kuzuha@gmail.com')
        password_input = self.selenium.find_element(By.NAME, 'password')
        password_input.send_keys('apopo1129')
        login_button = self.selenium.find_element(By.CLASS_NAME, 'btn')
        login_button.click()

        # ページタイトルの検証
        expected_title_part = 'Login|Private Diary'
        self.assertIn(expected_title_part, self.selenium.title)
