from pages.base_page import BasePage
from pages.base_elem import BasePageElement
from selenium.webdriver.common.by import By
import logging
import json


class LocatorsImageSearchPage:
    # текстовый запрос в строке поиска
    REQUEST = (By.XPATH, "//div[contains(@id, 'AdvancedSearch_inline')]")
    # список элементов категорий изображений
    POPULAR_CATEGORIES = (By.XPATH, "//div[contains(@class, 'PopularRequestList-Item')]")
    # всплывающее окно с защитой от Adblock
    INSTALL_POPUP_CLOSE = (By.XPATH, "//a[text()='Закрыть']//ancestor::div[4]")
    INSTALL_POPUP_INST = (By.XPATH, "//a[text()='Установить']//ancestor::div[4]")
    

class ImageSearchRequestContainer(BasePageElement):
    locator = LocatorsImageSearchPage.REQUEST


class ImageSearchPopularCategories(BasePageElement):
    locator = LocatorsImageSearchPage.POPULAR_CATEGORIES
    

class PopupWindowButtonClose(BasePageElement):
    locator = LocatorsImageSearchPage.INSTALL_POPUP_CLOSE
    timeout = 3


class PopupWindowButtonInstall(BasePageElement):
    locator = LocatorsImageSearchPage.INSTALL_POPUP_INST
    timeout = 3
    

class ImageSearchPage(BasePage):
    """
    Класс описывает страницу "поиск картинок"
    """
    request_container = ImageSearchRequestContainer('search')
    popular_category_list = ImageSearchPopularCategories('search_all')
    popup_window_button_close = PopupWindowButtonClose('search')
    popup_window_button_inst = PopupWindowButtonInstall('search')
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_search_field_text(self):
        logging.info('получить текст из поля поиска')
        search_field = self.request_container
        attrs = search_field.get_attribute('data-state')
        text_in_field = json.loads(attrs).get('query')
        return text_in_field

    def get_popular_category_name(self, cat_number):
        category = self.popular_category_list[cat_number]
        name = category.get_attribute('data-grid-text')
        logging.info(f'получить название категории изображений №{cat_number}')
        logging.info(f'название категории "{name}"')
        return name
    
    def select_popular_category(self, cat_number):
        button_close = self.popup_window_button_close
        button_install = self.popup_window_button_inst
        # обход защиты Adblock
        if button_close and (button_close == button_install):
            logging.info('удалить всплывающее окно "установка браузера Яндекс"')
            self.delete_node(button_close)
        logging.info(f'перейти к категории изображений {cat_number}')
        self.popular_category_list[cat_number].click()
        logging.info('ожидание загрузки')
        self.wait_for_page_loaded()
        self.wait_for_load_spinner()
