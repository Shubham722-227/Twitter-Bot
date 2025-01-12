from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys
from webdriver_manager.firefox import GeckoDriverManager
import time

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

class Twitter_Bot:

    """
    A Bot class that provide features of:
        - Logging into your Twitter account
        - Liking tweets of your homepage
        - Searching for some keyword or hashtag
        - Liking tweets of the search results
        - Posting tweets
        - Retweeting tweets
        - Logging out of your account

    ........

    Attributes
    
    ----------
    email : str
        user email for authentication of Twitter account
    password : str
        user password for authentication of Twitter account
    bot : WebDriver
        webdriver that carry out the automation tasks
    is_logged_in : bool
        boolean to check if the user is logged in or not

    Methods
    -------
    login()
        logs user in based on email and password provided during initialisation
    logout()
        logs user out
    search(query: str)
        searches for the provided query string
    like_tweets(cycles: int)
        loops over number of cycles provided, scrolls the page down and likes the available tweets on the page in each loop pass
    retweet(cycles: int)
        loops over number of cycles provided, scrolls the page down and retweets the available tweets on the page in each loop pass
    """
    

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.bot = driver
        self.bot.maximize_window()
        self.is_logged_in = False

    #Login Function 
    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login/')
        time.sleep(5)

        try:
            email = bot.find_element_by_name('session[username_or_email]')
            password = bot.find_element_by_name('session[password]')
        except common.exceptions.NoSuchElementException:
            time.sleep(5)
            email = bot.find_element_by_name('session[username_or_email]')
            password = bot.find_element_by_name('session[password]')

        email.clear()
        password.clear()
        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        time.sleep(10)
        self.is_logged_in = True
        
    #Logout Function
    def logout(self):
        if not self.is_logged_in:
            return 

        bot = self.bot
        bot.get('https://twitter.com/home')
        time.sleep(4)

        try:
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()

        time.sleep(1)

        try:
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()

        time.sleep(3)

        try:
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()

        time.sleep(3) 
        self.is_logged_in = False

        bot.close()

    #Search Function : Make searches based on keywords
    def search(self, query=''):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            searchbox = bot.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            searchbox = bot.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")

        searchbox.clear()
        searchbox.send_keys(query)
        searchbox.send_keys(keys.Keys.RETURN)
        time.sleep(10)  
        """
        url = "https://twitter.com/search?q=" + query
        bot.get(url)
        time.sleep(10)
        """

    #Function meant for liking tweets
    def like_tweets(self, cycles=10):
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        bot = self.bot

        for i in range(cycles):
            try:
                bot.find_element_by_xpath("//div[@data-testid='like']").click()
                #like.click()
            except common.exceptions.NoSuchElementException:
                time.sleep(3)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight/2.5)') 
                time.sleep(3)
                bot.find_element_by_xpath("//div[@data-testid='like']").click()
                #like.click()

            time.sleep(1)
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight/2.5)') 
            time.sleep(5)

    #This function retweets posts based on keywords
    def retweet(self,cycles=10):
        if not self.is_logged_in:
            raise Exception("You must log in first!")
        bot = self.bot

        for i in range(cycles):
            try:
                bot.find_element_by_xpath("//div[@data-testid='retweet']").click()
                time.sleep(1)
                bot.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
            except common.exceptions.NoSuchElementException:
                time.sleep(3)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight/2.5)')
                time.sleep(3)
                bot.find_element_by_xpath("//div[@data-testid='retweet']").click()
                time.sleep(1)
                bot.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
            time.sleep(1)
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight/2.5)')
            time.sleep(5)

    #Function to post tweets
    def post_tweets(self,tweetBody):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot  

        try:
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4) 
        body = tweetBody

        try:
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)

        time.sleep(4)
        bot.find_element_by_class_name("notranslate").send_keys(keys.Keys.ENTER)
        bot.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
        time.sleep(4) 

