from pages.base_page import BasePage
from pages.base_elem import BasePageElement
from selenium.webdriver.common.by import By
import logging


class LocatorsSearchResults:
    # страница с результатами поиска
    RESULT_CONTAINER = (By.ID, "search-result")
    # сами результаты поиска, локатор исключает попадание в список результатов без ссылок
    RESULTS_LIST = (By.XPATH, "//li[contains(@class, 'serp-item serp-item_card')]/descendant::a[1]")


class SearchResultsContainer(BasePageElement):
    locator = LocatorsSearchResults.RESULT_CONTAINER


class SearchResultList(BasePageElement):
    locator = LocatorsSearchResults.RESULTS_LIST


class SearchResultPage(BasePage):
    """
    Класс описывает страницу с результатами поиска
    """
    search_result_container = SearchResultsContainer('search')
    search_result_elements = SearchResultList('search_all')
    
    def __init__(self, driver):
        super().__init__(driver)
        
    @staticmethod
    def get_search_result_link(search_result):
        logging.info(f'получить href элемента {search_result}')
        return search_result.get_attribute('href')
