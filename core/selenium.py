from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By


geckopath = '/usr/bin/geckodriver'
ffbinaryx = '/usr/bin/firefox'

class SeleniumBrowser():
    def __init__(self, url=None):
        self.driver = None
        self.url = url

    def activate(self):
        if isinstance(self.driver, Firefox):
            return self.driver
        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(ffbinaryx), executable_path=geckopath, options=opts)
        #return self.driver

    def open_main_page(self):
        self.driver.get(self.url)

    def open_page(self, url):
        self.driver.get(url)

    def get_page(self, page_number):
        if self.driver:
            if not page_number > 1:
                self.driver.get(self.url)
                return self.driver.page_source.encode('utf-8')
        else:
            raise Exception('Не запущен браузер')

    def get_page_source(self):
        return BeautifulSoup(self.driver.page_source.encode('utf-8'), 'html.parser')

    def get_paginate_number_element(self, number):
        pagination_ul = self.driver.find_elements(By.CLASS_NAME, 'm-pagination')
        pagination_buttons = self.driver.find_elements(By.CLASS_NAME, 'paginatenum')
        return pagination_buttons[number - 1]

    def click_to_button(self, element):
        element.click()

    def quit(self):
        self.driver.quit()
        self.driver = None