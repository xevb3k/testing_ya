from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging

DEFAULT_TIMEOUT = 10


class BasePageElement:
    """
    Класс описывает дескриптор элемента страницы
    """
    action_list = {
                   # возврат 1 элемента
                   'search': EC.presence_of_element_located,
                   # возврат списка элементов
                   'search_all': EC.presence_of_all_elements_located,
                   
                   # возвращает элемент если он есть и видим, иначе False
                   'is_visible': EC.visibility_of_element_located,
                   
                   # возвращает элемент, если он НЕ видим,
                   # True если элемента нет или он устарел, False если он видим
                   'is_invisible': EC.invisibility_of_element_located
    }

    locator = None
    timeout = DEFAULT_TIMEOUT

    def __init__(self, action):
        super().__init__()
        self.action_name = action
        self.action = self.action_list.get(action)

    def __get__(self, instance, owner):
        if self.action_name in list(self.action_list)[:2]:
            try:
                logging.info(f'получить элемент {self.locator}')
                logging.info(f'действие {self.action_name}')
                logging.info(f'таймаут {self.timeout}')
                elem = WebDriverWait(instance.driver, self.timeout).\
                    until(self.action(self.locator))
            except TimeoutException:
                logging.warning(f'элемент не найден по таймауту {self.locator}')
                return None
            return elem
        else:
            logging.info(f'запросить статус элемента {self.locator}')
            logging.info(f'действие {self.action_name}')
            elem = WebDriverWait(instance.driver, self.timeout). \
                until(self.action(self.locator))
            return elem
            
    def __set__(self, instance, value):
        logging.info(f'установить значение "{value}" элементу {self.locator}')
        WebDriverWait(instance.driver, self.timeout).\
            until(EC.presence_of_element_located(self.locator)).send_keys(value)
