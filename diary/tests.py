# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# class TestHomePage(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Safari WebDriverを使用します
#         super().setUpClass()
#         cls.browser = webdriver.Safari()

#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.quit()
#         super().tearDownClass()

#     def test_homepage(self):
#         # ホームページを開く
#         self.browser.get('self.live_server_url')

#         # ページのタイトルを確認
#         self.assertIn('Private Diary', self.browser.title)
