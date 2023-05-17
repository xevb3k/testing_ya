from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pages.base_elem import BasePageElement
import time
import logging


class LocatorsImageSearchPage:
    # общий элемент для всех страниц - спиннер подгрузки
    LOAD_SPINNER = (By.XPATH, "//div[contains(@class, 'Spinner')]")
    

class LoadSpinner(BasePageElement):
    locator = LocatorsImageSearchPage.LOAD_SPINNER
    timeout = 1
    

class BasePage:
    """
    Базовый класс для страниц сайта
    """
    DEFAULT_TIMEOUT = 10
    
    load_spinner = LoadSpinner('search')
    
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://ya.ru/'

    def _get_elem_attributes(self, element) -> dict:
        """
        Возвращает список всех атрибутов элемента
        :param element: вебэлемент
        :return: словарь атрибутов
        """
        return self.driver.execute_script(
            """
            let attr = arguments[0].attributes;
            let items = {};
            for (let i = 0; i < attr.length; i++) {
                items[attr[i].name] = attr[i].value;
            }
            return items;
            """, element)

    def open_page(self):
        """
        Открыть url в браузере self.driver
        """
        logging.info(f'открыть страницу {self.url}')
        self.driver.get(self.url)

    def get_current_url(self):
        """"
        Возвращает текущий url
        """
        url = self.driver.current_url
        logging.info(f'получен текущий url {url}')
        return url

    def goto_link(self, link, timeout=DEFAULT_TIMEOUT):
        """
        Переходит по ссылке, определяет фактический URL, закрывает открывшуюся вкладку и переходит к предыдущей вкладке
        :param link: WebElement, содержащий href
        :param timeout: таймаут
        :return: фактический URL, если удачно перешли
        """
        old_window_handle = self.driver.current_window_handle
        old_windows_handles = self.driver.window_handles
        logging.info('переход по ссылке')
        link.click()
        logging.info('ожидание открытия новой вкладки')
        WebDriverWait(self.driver, timeout).until(EC.new_window_is_opened(old_windows_handles))
        window_handle_list = self.driver.window_handles
        new_link = ''
        for handle in window_handle_list:
            if handle != old_window_handle:
                logging.info(f'переключение контекста драйвера на окно {handle}')
                self.driver.switch_to.window(handle)
                self.wait_for_page_loaded()
                new_link = self.get_current_url()
                logging.info(f'получен новый url {new_link}')
                logging.info('закрыть вкладку')
                self.driver.close()
        logging.info(f'переключение контекста драйвера на окно {old_window_handle}')
        self.driver.switch_to.window(old_window_handle)
        return new_link
    
    def switch_to_new_window(self):
        """
        Переключение контекста драйвера на последнюю открытую вкладку
        """
        new_window = self.driver.switch_to.window(self.driver.window_handles[-1])
        logging.info(f'переключение на окно {new_window}')
        
    def delete_node(self, node):
        logging.info(f'удаление узла {node}')
        self.driver.execute_script("arguments[0].remove();", node)
    
    def wait_for_page_loaded(self):
        logging.info('ожидание загрузки страницы')
        while True:
            time.sleep(0.5)
            if self.driver.execute_script("return document.readyState == 'complete';"):
                break
        logging.info('страница загружена')
        
    def wait_for_load_spinner(self):
        logging.info('ожидание полной загрузки изображений')
        while self.load_spinner:
            time.sleep(0.1)
        logging.info('изображения загружены')
        