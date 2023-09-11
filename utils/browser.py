# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from .p_system import sys_info


def init_driver(driver_name: str, headless: bool):
    if driver_name == 'chrome':
        return chrome_driver(headless)


def firefox_driver(headless):
    ...


def chrome_driver(headless):
    service = Service(f'{sys_info()}/browser/chromedriver.exe')
    options = webdriver.ChromeOptions()
    if headless is True:
        # 无头设置
        options.add_argument('--headless')

    options.add_argument("--disable-blink-features")
    # ua
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver
