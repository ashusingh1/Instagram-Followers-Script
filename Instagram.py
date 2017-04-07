from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Instagram:

    def __init__(self, username=None, passw=None):
        self.__username = username
        self.__password = passw
        self.__nfollowers = 0
        self.__nfollowing = 0
        self.__list_followers = []
        self.__list_following = []
        self.__non_followers = []
        self.__chrome = webdriver.Firefox()
        self.__chrome.get("http://instagram.com")
        assert "Instagram" in self.__chrome.title

        sleep(2)

        # log with an existent account
        self.__chrome.find_element_by_xpath("//a[@class='_fcn8k']").click()

        name = self.__chrome.find_element_by_name("username")
        passw = self.__chrome.find_element_by_name("password")

        if self.__username is not None and self.__password is not None:
            # enter username and password
            name.send_keys(self.__username)
            passw.send_keys(self.__password)
        else:
            print "User is not defined"

        # enter key is pressed to log in
        passw.send_keys(Keys.RETURN)
        # wait to load the page
        sleep(3)

    def open_profile(self):
        self.__chrome.find_element_by_xpath("//a[contains(@class,'coreSpriteDesktopNavProfile')]").click()
        sleep(2)

        self.__nfollowers = self.__chrome.find_element_by_xpath("//a[contains(@href,'/" + self.__username + "/followers/')]/span[@class='_bkw5z']").get_attribute('innerHTML')
        self.__nfollowing = self.__chrome.find_element_by_xpath("//a[contains(@href,'/" + self.__username + "/following/')]/span[@class='_bkw5z']").get_attribute('innerHTML')

    def get_followers(self):

        # abre popup dos seguidores
        self.__chrome.find_element_by_xpath("//a[contains(@href,'/"+self.__username+"/followers/')]").click()

        sleep(2)

        popup_followers = self.__chrome.find_element_by_xpath("//div[contains(@class,'_4gt3b')]")
        popup_followers.click()

        #carrega todos os que me seguem
        for _ in range(10, int(self.__nfollowers), 10):
            popup_followers.send_keys(Keys.PAGE_DOWN)
            popup_followers.send_keys(Keys.PAGE_DOWN)
            sleep(1)

        elements_followers = self.__chrome.find_elements_by_xpath("//a[contains(@class,'_4zhc5')]")
        self.__list_followers = map(lambda x: x.get_attribute('innerHTML'), elements_followers)

        # testa se leu todos os seguidores
        assert len(self.__list_followers) == int(self.__nfollowers), "Failed loading all followers"

        self.__chrome.find_element_by_xpath("//div[@class='_quk42']").send_keys(Keys.ESCAPE)

    def get_following(self):
        self.__chrome.find_element_by_xpath("//a[contains(@href,'/"+self.__username+"/following/')]").click()

        sleep(2)

        popup_following = self.__chrome.find_element_by_xpath("//div[contains(@class,'_4gt3b')]")
        popup_following.click()

        # carrega todos os que sigo
        for _ in range(10, int(self.__nfollowing), 10):
            popup_following.send_keys(Keys.PAGE_DOWN)
            popup_following.send_keys(Keys.PAGE_DOWN)
            sleep(1)

        elements_following = self.__chrome.find_elements_by_xpath("//a[contains(@class,'_4zhc5')]")
        self.__list_following = map(lambda x: x.get_attribute('innerHTML'), elements_following)

        assert len(self.__list_following) == int(self.__nfollowing), "Failed load all following"

        self.__chrome.find_element_by_xpath("//div[@class='_quk42']").send_keys(Keys.ESCAPE)

    def get_non_followers(self):
        self.open_profile()
        self.get_followers()
        self.get_following()

        print "PEOPLE WHO DONT FOLLOW YOU BACK:"
        for following in self.__list_following:
            if following not in self.__list_followers:
                print following
                self.__non_followers.append(following)


