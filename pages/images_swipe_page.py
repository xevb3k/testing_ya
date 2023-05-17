from pages.base_page import BasePage
from pages.base_elem import BasePageElement
from selenium.webdriver.common.by import By
import logging


class LocatorsImageSwipeModalWindow:
    # модальное окно со слайдером изображений
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'ImagesViewer-Container')]")
    # превью изображения в слайдере
    SWIPE_PREVIEW = (By.XPATH, "//img[contains(@class, 'MMImage-Preview')]")
    # кнопки слайдер вправо-влево
    BUTTON_NEXT = (By.XPATH, "//div[contains(@class, 'CircleButton_type_next')]")
    BUTTON_PREV = (By.XPATH, "//div[contains(@class, 'CircleButton_type_prev')]")
    # кнопка закрытия модального окна
    CLOSE_BUTTON = (By.XPATH, "//div[contains(@class, 'MMViewerModal-Close')]")


class ImageSwipeModalContainer(BasePageElement):
    locator = LocatorsImageSwipeModalWindow.MODAL_CONTAINER
    
    
class ImageSwipePreview(BasePageElement):
    locator = LocatorsImageSwipeModalWindow.SWIPE_PREVIEW
    

class ImageSwipeButtonNext(BasePageElement):
    locator = LocatorsImageSwipeModalWindow.BUTTON_NEXT


class ImageSwipeButtonPrev(BasePageElement):
    locator = LocatorsImageSwipeModalWindow.BUTTON_PREV
    

class ImageSwipeButtonCloseModal(BasePageElement):
    locator = LocatorsImageSwipeModalWindow.CLOSE_BUTTON
    

class ImageSwipeModalWindow(BasePage):
    """
    Класс описывает страницу с модальным окном - слайдером картинок
    """
    modal_window = ImageSwipeModalContainer('search')
    swipe_preview = ImageSwipePreview('search')
    button_next = ImageSwipeButtonNext('search')
    button_prev = ImageSwipeButtonPrev('search')
    close_button = ImageSwipeButtonCloseModal('search')
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def next_button_click(self):
        logging.info('нажать кнопку вперед')
        self.button_next.click()
        logging.info('ожидание загрузки')
        self.wait_for_load_spinner()
        
    def prev_button_click(self):
        logging.info('нажать кнопку назад')
        self.button_prev.click()
        logging.info('ожидание загрузки')
        self.wait_for_load_spinner()

    def get_swipe_preview_url(self):
        logging.info('получить src открытого изображения')
        image_link = self.swipe_preview.get_attribute('src')
        return image_link
