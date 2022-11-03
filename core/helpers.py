from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.selenium import SeleniumBrowser
from selenium.common.exceptions import TimeoutException


def get_game_card(element):
    return 'm-product-placement-item' in element['class']


class SeleniumMixin:
    def get_page(self, page_url):
        sel = SeleniumBrowser()
        sel.activate()
        sel.open_page(page_url)
        page = sel.driver.page_source.encode('utf-8')
        sel.quit()
        return page

    def get_page_with_delay(self, page_url, delay, until):
        sel = SeleniumBrowser()
        sel.activate()
        sel.open_page(page_url)
        try:
            WebDriverWait(sel.driver, delay).until(until)
        except TimeoutException:
            sel.quit()
            raise TimeoutException('Не улалось найти элемент на страниц')
        page = sel.driver.page_source.encode('utf-8')
        sel.quit()
        return page

class PageSoup(SeleniumMixin):

    def get_by_tag_and_class(self, page_url, class_name, tag):

        page_source = self.get_page_with_delay(page_url, 3, EC.presence_of_element_located((By.CLASS_NAME, class_name)))

        page = BeautifulSoup(page_source, 'html.parser')
        elements = page.find_all(tag, {"class": class_name})
        return elements

    def get_by_text(self, element, text):
        element.find('span', {"class": 'ProductCard-module__title___3iwfs'})

    @staticmethod
    def get_childs(element, **kwargs):
        childs = list(element.findChildren(kwargs['tag'],recursive=True))
        return childs

page_soup = PageSoup()