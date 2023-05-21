import os
import time
import configparser
from src.retrieveMail import verification_code
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.constants.paths import IAESTE_PLATFORM_LOGIN_CREDENTIALS

# Define element references for click actions
ELEMENT_REFERENCE_TABLE = {
    'login_button': [By.XPATH, '//input[@type="submit"]'],
    'submit_button': [By.XPATH, '//input[@type="button" and @value="Submit"]'],
    'csv_dropdown': [By.XPATH, '//a[contains(text(), "CSV")]'],
    'export_button': [By.XPATH, '//a[@id="1497"]'],
    'file_export_button': [By.XPATH, '//a[@id="btn_fileexp"]']
}


class ForeignOffersExtractor():
    """A class for automatically downloading CSV files from the IAESTE website 
    using Selenium."""

    def __init__(self, loginPage='https://iaeste.smartsimple.ie/s_Login.jsp'):
        """Constructor for the ForeignOffersExtractor class.
        
        Args:
            loginPage (str): The URL of the IAESTE login page.
        """
        self.loginPage = loginPage
        self.saveLocation = os.getcwd()
        self.email, self.password = self._getLoginCredentials()
        self.driver = self._initialiseDriver()

    def _element_clicker(self, element: str):
        """Click on an element on the page.
        
        Args:
            element (str): The name of the element to click on.
        """
        byType, searchString = ELEMENT_REFERENCE_TABLE[element]
        temp_element = self.driver.find_element(byType, searchString)
        temp_element.click()

    def _find_all_iframes(self):
        """Recursively search for the file export button within all the iframes 
        on the page."""
        iframes = self.driver.find_elements(By.XPATH, "//iframe")
        for index, iframe in enumerate(iframes):
            self.driver.switch_to.frame(index)
            if 'btn_fileexp' in self.driver.page_source:
                self._element_clicker('file_export_button')
                return
            self._find_all_iframes()
            self.driver.switch_to.parent_frame()

    def _getLoginCredentials(self):
        """Get the login credentials for IAESTE from the configuration file."""
        config = configparser.ConfigParser()
        config.read(
            IAESTE_PLATFORM_LOGIN_CREDENTIALS
        )
        email = config.get('login', 'email').strip("'")
        password = config.get('login', 'password').strip("'")
        return email, password

    def _initialiseDriver(self):
        """Initialise the Selenium webdriver."""
        # set the download directory to the current working directory
        chrome_options = Options()
        chrome_options.add_experimental_option(
            'prefs', {'download.default_directory': f'{self.saveLocation}'})
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # create the webdriver with the options
        return webdriver.Chrome(options=chrome_options)

    def _login(self):
        """Log in to the IAESTE website."""
        # navigate to the login page
        self.driver.get(self.loginPage)

        # find the email and password fields and enter your login credentials
        email_field = self.driver.find_element(By.NAME, 'user')
        password_field = self.driver.find_element(By.NAME, 'password')
        email_field.send_keys(self.email)
        password_field.send_keys(self.password)

        # click on the login button
        self._element_clicker('login_button')

        # wait for the dashboard to load
        dashboard_title = WebDriverWait(self.driver, 10)

    def _verification(self, code: int):
        """Verify login on the IAESTE website."""

        # find the email and password fields and enter your login credentials
        code_field = self.driver.find_element(By.NAME, 'tokenpin')
        code_field.send_keys(code)

        # click on the login button
        self._element_clicker('submit_button')

    def getCSV(self):
        # time.sleep values are set to work with a raspberry pi 3, change as 
        # needed. Faster systems will require much less waiting time.
        self.driver.maximize_window()
        self._login()
        time.sleep(10)

        code = verification_code()
        self._verification(code)

        # Click on the CSV dropdown and wait for the Export button to appear
        time.sleep(60)
        self._element_clicker('csv_dropdown')
        time.sleep(10)
        self._element_clicker('export_button')
        time.sleep(30)

        # Wait for the file export button to appear in any iframe and click it
        self._find_all_iframes()

        # Wait for the file to finish downloading and then quit the driver
        time.sleep(60)
        self.driver.quit()
