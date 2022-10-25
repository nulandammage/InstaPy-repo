from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from all_secrets import username, password


class InstaBot:

    def __init__(self, username, password):
        self.blacklist = []
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'))

    def login(self):
        self.browser.implicitly_wait(10)
        self.browser.get('https://www.instagram.com/')
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        time.sleep(5)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]').click()

    def find_not_following(self):
        self.browser.implicitly_wait(10)
        follower_number = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        self.follower_names = self._get_names(follower_number, "//div[@role='dialog']//a")
        self.browser.implicitly_wait(10)
        self.following_number = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        self.following_names = self._get_names(self.following_number, "//div[@role='dialog']//a")
        print(self.following_names)
        print("#########################################")
        print(self.follower_names)
        self.blacklist = [person for person in self.following_names if person not in self.follower_names]
        return self.blacklist

    def _get_names(self, number, scroll_window_xpath):
        self.browser.implicitly_wait(10)
        counter = 0
        number = int(number)
        while counter < int(number / 5):
            scrollwindow = self.browser.find_element_by_xpath(scroll_window_xpath)
            scrollwindow.send_keys(Keys.PAGE_DOWN)
            counter += 1
            time.sleep(0.5)
        links = self.browser.find_elements_by_xpath('//*[@id="f358d8763265bd4"]')
        accounts = [account.get_attribute('title') for account in links]
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return accounts

    def unfollow_people(self, names):
        if type(names) is not list:
            names = list(names)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        self.scroll_window = self.browser.find_element_by_xpath("//div[@role='dialog']//a")
        counter = 0
        while counter < int(int(self.following_number) / 5):
            self.scroll_window.send_keys(Keys.PAGE_DOWN)
            counter += 1
            time.sleep(0.5)
        self.unfollow_buttons = self.browser.find_element_by_xpath("//button[@class='oF4XW sqdOP  L3NKy   _8A5w5   ']")
        self.browser.implicitly_wait(10)
        for account in names:
            self.unfollow_buttons[self.following_names.index(str(account))].click()
            time.sleep(0.5)
            self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
            time.sleep(1.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button/div/svg').click()


if __name__ == "__main__":
    bot = InstaBot(username, password)
    bot.login()
    time.sleep(5)
    print(bot.find_not_following())
    bot.browser.close()


# login working
