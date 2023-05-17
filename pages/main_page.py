from pages.base_page import BasePage
from pages.base_elem import BasePageElement
from selenium.webdriver.common.by import By
import logging


class LocatorsMainPage:
    # поле поиска
    SEARCH_FIELD = (By.XPATH, "//input[contains(@class, 'search3__input')]")
    # набор элементов с подсказками результатов поиска
    SUGGEST_SEARCH_PROMPT_LIST = (By.XPATH, "//li[contains(@id, 'suggest-item')]")
    # кнопка Еще всплывающего меню
    SUGGEST_BUTTON_MORE = (By.XPATH, "//a[contains(@class, 'services-suggest__item-more')]")
    # главное меню
    MAIN_MENU_POPUP = (By.XPATH, "//div[contains(@class, 'popup2_visible_yes')]")
    # кнопка "Картинки" главного меню
    MAIN_MENU_IMAGES_BUTTON = (By.XPATH, "//a[contains(@aria-label, 'Картинки')]")
    # модальное окно с уведомлением (для закрытия)
    MODAL_POPUP = (By.XPATH, "//div[contains(@class, 'modal__content')]/ancestor::div[4]")


class SearchField(BasePageElement):
    locator = LocatorsMainPage.SEARCH_FIELD


class SuggestSearchPrompt(BasePageElement):
    locator = LocatorsMainPage.SUGGEST_SEARCH_PROMPT_LIST


class SuggestMenuButtonMore(BasePageElement):
    locator = LocatorsMainPage.SUGGEST_BUTTON_MORE


class MainMenu(BasePageElement):
    locator = LocatorsMainPage.MAIN_MENU_POPUP


class MainMenuImagesButton(BasePageElement):
    locator = LocatorsMainPage.MAIN_MENU_IMAGES_BUTTON
    
    
class ModalPopup(BasePageElement):
    locator = LocatorsMainPage.MODAL_POPUP
    timeout = 2
    

class MainPage(BasePage):
    """
    Класс описывает главную страницу ya.ru
    """
    search_field_new = SearchField('search')
    suggest_search_prompt_list = SuggestSearchPrompt('is_visible')
    suggest_menu_more_button = SuggestMenuButtonMore('is_visible')
    main_menu = MainMenu('search')
    main_menu_images_button = MainMenuImagesButton('search')
    modal_popup = ModalPopup('search')
    
    def __init__(self, driver):
        super().__init__(driver)
   
    def main_menu_images_button_click(self):
        logging.info('переход по кнопке главного меню "Изображения"')
        self.main_menu_images_button.click()
        self.switch_to_new_window()
        self.wait_for_page_loaded()
        self.wait_for_load_spinner()
        return self.get_current_url()

    def open_main_page(self):
        self.open_page()
        self.wait_for_page_loaded()
        
        # удалить всплывающее окно, если есть
        popup = self.modal_popup
        if popup:
            logging.info('удалить всплывающее модальное окно')
            self.delete_node(popup)
        