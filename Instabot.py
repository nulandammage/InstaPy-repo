import time
import random
from getpass import getpass
from datetime import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

## once done testing run with options as it is faster and the browser does not pop up

options = Options()
options.add_argument('--headless')

class InstaBot:

    def __init__(self, path_to_driver):
        self.path = path_to_driver
        self.url = "https://www.instagram.com/"
        self.browser = Firefox(executable_path=self.path) #options=options)
        self.__username, self.__password = self.__getUsername()
        self.followers, self.following, self.unfollow_buttons, self.not_following_back = [], [], [], []
        self.max_count = 10

    def login(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)
        
        # find the username and password boxes in the website and enter the username and password
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(self.__username)
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(self.__password)
        
        # find the login button and click it 
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div").click()

        # find and click the not now on save login info and the notifications buttons
        self.browser.implicitly_wait(5)
        try:
            self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        except Exception as e:
            print(e)

        self.browser.implicitly_wait(5)
        try:
            self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")
        except Exception as e:
            print(e)

        # move to the userpage
        self.browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
        self.browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div").click()

    def _getNotFollowing(self, full=True):
        time.sleep(3)
        if not full and not self.followers:
            self.followers = self._contentsOfScrollBox(False, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
        time.sleep(3)
        self.following, self.unfollow_buttons = self._contentsOfScrollBox(True, "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        self.not_following_back = set(self.following) - set(self.followers)
        

    def _contentsOfScrollBox(self, track_buttons, xpath_to_scrollbar):
        # open the scroll box
        self.browser.find_element_by_xpath(xpath_to_scrollbar).click()
        self.browser.implicitly_wait(5)
        #self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a").click()
        self.scroll_bar = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_height, next_height = 1, 0
        while last_height != next_height:
            last_height = next_height
            time.sleep(2)
            next_height = self.firefox_browser.execute_script("""
                          arguments[0].scrollTo(0, arguments[0].scrollHeight);
                          return arguments[0].scrollHeight""", self.scroll_bar)

        links = self.scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        if track_buttons:
            # close the scroll box
            buttons = self.scroll_box.find_elements_by_xpath("//button[text()='Following']")
            self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
            return names, buttons
        # close the scroll box
        self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
        return names

    def unfollowUsers(self, ignore):
        for _ in range(self.max_count):
            self.browser.implicitly_wait(5)
            names = [name for name in list(self._getNotFollowing(False)) if name not in ignore]
            self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a").click()
            for account in names:
                try:
                    self.unfollow_buttons[self.following.index(account)].click()
                    time.sleep(random.randint(2, 6))
                    self.browser.find_element_by_xpath("//button[@class='aOOlW -Cab_   '").click()
                    time.sleep(random.randint(2, 6))
                except Exception as e:
                    print(e)
                self.browser.refresh()
                time.sleep(random.randint(5, 16))

    def __getUsername(self):
        return input("Input your username: "), getpass("Enter your password: ")

