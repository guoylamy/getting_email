from selenium import webdriver
import selenium.webdriver.chrome.options as chrome_options
import selenium.webdriver.firefox.options as firefox_options


# For Windows
PATH_CHROME_DRIVER=r"chromedriver.exe"
PATH_FIREFOX_DRIVER=r"geckodriver.exe"


def get_headless_chrome():
    options = chrome_options.Options()
    options.headless = True
    #options.add_argument('user-data-dir=C:/Users/Tu Le/AppData/Local/Google/Chrome/User Data/Default')
    driver = webdriver.Chrome(options=options, executable_path=PATH_CHROME_DRIVER)
    # driver.implicitly_wait(100)
    return driver


def get_firefox():
    options = firefox_options.Options()
    options.headless = True
    fp = webdriver.FirefoxProfile('C:/Users/Tu Le/AppData/Roaming/Mozilla/Firefox/Profiles/ejmvt067.default-1554669393168')
    driver = webdriver.Firefox(options=options, firefox_profile=fp, executable_path=PATH_FIREFOX_DRIVER)
    return driver