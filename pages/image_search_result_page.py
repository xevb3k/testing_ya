from pages.base_page import BasePage
from pages.base_elem import BasePageElement
from selenium.webdriver.common.by import By
import logging
import json


class LocatorsImageSearchResultPage:
    # список элементов результата поиска
    RESULTS_LIST = (By.XPATH, "//div[contains(@class, 'serp-item_type_search')]")


class ImageSearchResults(BasePageElement):
    locator = LocatorsImageSearchResultPage.RESULTS_LIST


class ImageSearchResultPage(BasePage):
    """
    Класс описывает страницу с результатами поиска картинок
    """
    image_search_result = ImageSearchResults('search_all')

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_load_spinner()

    def select_search_result(self, result_number):
        logging.info(f'выбрать найденное изображение №{result_number}')
        self.image_search_result[result_number].click()
        logging.info('ожидание загрузки')
        self.wait_for_load_spinner()

    def get_search_result_url(self, result_number):
        logging.info(f'получить url изображения №{result_number}')
        attr = self.image_search_result[result_number].get_attribute('data-bem')
        attr_jsn = json.loads(attr)
        url = attr_jsn.get('serp-item').get('preview')[0].get('url')
        logging.info(f'url изображения: {url}')
        return url
