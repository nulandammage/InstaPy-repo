import os
from selenium import webdriver
from time import sleep
from all_secrets import password, username
from random import randint


class InstagramBot:
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'))
        self.browser.implicitly_wait(10)
        self.browser.get('https://www.instagram.com/')
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        sleep(5)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]').click()

        sleep(4)

    def get_not_following(self):
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        self.followers = self._get_names()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        self.following = self._get_names()
        print(len(self.following) - len(self.followers))
        self.not_following_back = [user for user in self.following if user not in self.followers]
        sleep(4)
        print(len(self.not_following_back))

    def _get_names(self):
        sleep(2)
        scroll_box = self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(3)
            ht = self.browser.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return names

    def unfollow_people(self, names):
        if type(names) is not list:
            names = list(names)
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        scroll_box = self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(3)
            ht = self.browser.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        self.unfollow_buttons = scroll_box.find_elements_by_xpath("//button[@class='oF4XW sqdOP  L3NKy   _8A5w5   ']")
        print(self.unfollow_buttons)
        
        # close button
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()

if __name__ == "__main__":
    my_bot = InstagramBot(username=username, password=password)
    my_bot.get_not_following()
    my_bot.unfollow_people('names')
    my_bot.browser.close()