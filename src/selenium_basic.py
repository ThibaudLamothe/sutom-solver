import os
import time
import random
from tkinter.tix import Tree
import logzero
import logging
from logzero import logger as lg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class SeleniumBasic:
    """ Skeleton for apps using Selenium. Frequently needed shortcuts are available in here.
    """

    def __init__(self, driver_path='chromedriver', loglevel='error'):
        """Instanciate the class needs to feed a selenium driver.
           (Development realized on macOS Catalina + Chrome)
        
        PARAMETERS:
            - driver_path : str - path to the selenium driver (mandatory)
            - loglevel    : str - [debug/info/warning/error] (default is error). Adapt the level of information displayed in terminal.
        """
        
        # Parameters
        self.url = None
        self.original_window = None
        self.display_sleep_time=False
        
        # Driver
        self.driver_path = driver_path
        self.driver_ok = self.create_driver()
        self.driver_advice = False
        # Log
        self.set_loglevel(loglevel)
    

    def create_driver(self):
        """Instanciate 
        """

        lg.info("Driver instanciation...")
        lg.info(f"Looking @ {self.driver_path}")
        if not os.path.exists(self.driver_path):
            lg.error("Driver not found.")
            return False

        chrome_options = Options()
        chrome_options.add_argument("--lang=fr-FR")
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=chrome_options) 
        lg.info('Driver found & loaded.')
        return True

    
    def check_driver(self):
        if self.driver_ok:
            return True
        
        if not self.driver_advice:
            lg.error("Driver was not found. Be sure you have one (and the correct one).")
            lg.error("Check chrome version @ chrome://settings/help")
            lg.error("Download @ https://chromedriver.chromium.org/downloads")
        self.driver_advice = True


    def connect_to_url(self, url):
        """ Redirect the webpage to a new url.
        PARAMETERS:
            - url : str - webpage to visit with webdriver.
        """

        lg.info("Connexion to url...")
        lg.info(f"Request @ {url}")
        self.url = url
        self._load_url()  
        lg.info('URL loaded..')


    def _load_url(self, sleep=3):
        """Instantiate a new driver instance.

        PARAMETERS:
            - sleep : int - number of waiting seconds after instantiating driver. Default is 3.
        """

        self.driver.get(self.url)
        # self.original_window =  self.driver.window_handles[0]
        self.sleep(sleep, 'Load url : {}'.format(self.url))
        

    def paste_clipboard(self, element, os='macos', driver='chrome'):
        """ Copy clipboard content into the selected element

        PARAMETERS:
            - element : selenium element
            - os      : str - not used
            - driver  : strt - not used
        
        NO OUTPUT.
        """

        # element.send_keys(Keys.SHIFT, Keys.INSERT)
        element.send_keys(Keys.CONTROL, 'v')


    def scroll_to_element(self, elmt, sleep=1):
        """Scroll to any defined element on the webpage (essentially to make it clickcable).
        
        PARAMETERS:
            - elmt : selenium element - element to scroll to
            - sleep : int - number of waiting seconds after scrolling. Default is 1.
        """

        y = elmt.location['y']
        lg.debug('scrolling to y={}'.format(y))
        y = y - 150
        self.driver.execute_script("window.scrollTo(0, {})".format(y))
        self.sleep(sleep)


    def sleep(self, sleep=1, message='Wait', exact=False):
        """ Sleeping function : as web pages might take time to react, it is interesting to wait for their responses.
            To introduce noise the time value is slightly modified around the desired value.
        PARAMETERS:
            - sleep   : int - number of waiting seconds. Default is 1.
            - message : message to display in terminal (in addition to the waiting time). Displayed only when loglevel is debug or info.
            - exact   : boolean - To use the exact waitting value. Default is False: random noise of max 0.5s and minimum waiting time is 1s.
        """

        if self.display_sleep_time:
            lg.debug('({} s.) - {}'.format(sleep, message))
        
        if not exact:
            noise = random.random() - 0.5
            sleep = max(sleep + noise, 1)
        time.sleep(sleep)


    def close_driver(self):
        """ Close the driver instance and the window associated.
            Might be useful in case of bug or wrong instanciation.
        """
        if not self.check_driver():
            lg.error("Pas de driver. Pas de fermeture.")
            return False
        lg.info('Exit navigation.')
        self.driver.quit()
        

    def set_loglevel(self, level):
        """ Adapting the loglevel for information display through process.

        PARAMETERS:
            - loglevel : str - [debug/info/warning/error]
        """
        level_table = {
            'debug':logging.DEBUG,
            'warn':logging.WARNING,
            'warning':logging.WARNING,
            'info':logging.INFO,
            'error':logging.ERROR
        }
        loglevel = level_table[level.lower()]
        logzero.loglevel(loglevel)
        lg.info(f"Loglevel set @ {level}")
