import time
from pages.main_page import MainPage
from pages.image_search_page import ImageSearchPage
from pages.image_search_result_page import ImageSearchResultPage
from pages.images_swipe_page import ImageSwipeModalWindow
import pytest
import allure
import logging

valid_url = 'https://yandex.ru/images/'

# category_num, search_result_num, expected_link
test_data_1 = [(0, 0, valid_url)]


@allure.title('Поиск в Яндекс-Картинках')
@allure.feature('suggest menu')
@allure.feature('main menu')
@allure.feature('image search')
@allure.feature('image view')
@allure.feature('image swipe')
@allure.description('Переход со страницы ya.ru на ya.ru/images через suggest->main menu, поиск картинок из первой '
                    'популярной категории, просмотр первой картинки из результатов поиска, листание картинок')
@pytest.mark.headless_mode(False)
@pytest.mark.parametrize("category_num, search_result_num, expected_link", test_data_1, ids=['test_set_1'])
def test_images(firefox_browser, category_num, search_result_num, expected_link):
    logging.info('тест "поиск в Яндекс-Картинках"')
    browser = firefox_browser
    
    with allure.step(f'Открыть страницу'):
        main_page = MainPage(browser)
        main_page.open_main_page()
    
    with allure.step('Проверка наличия поля поиска'):
        assert main_page.search_field_new, 'не найдено поле поиска'
    
    with allure.step('Проверка наличия всплывающего меню при фокусе на поле поиска'):
        main_page.search_field_new.click()
        assert main_page.suggest_menu_more_button, 'нет всплывающей навигационной панели'
    
    with allure.step('Проверка открытия главного меню при клике на кнопку "Все"'):
        main_page.suggest_menu_more_button.click()
        assert main_page.main_menu, 'не открылось главное меню'
    
    with allure.step(f'Проверка что произошел переход на {expected_link} при клике на кнопку "Картинки"'):
        url = main_page.main_menu_images_button_click()
        assert url in expected_link, f'не произошел переход на {expected_link}'
    
    image_search_page = ImageSearchPage(browser)
    
    with allure.step(f'Выбор {category_num}й категории из списка популярных'):
        first_category_name = image_search_page.get_popular_category_name(category_num)
        image_search_page.select_popular_category(category_num)
    
    with allure.step('Проверка что название выбранной категории отображается в поле поиска'):
        image_search_field_text = image_search_page.get_search_field_text()
        assert first_category_name == image_search_field_text, 'название категории не отображается в поле поиске'
    
    images_search_result_page = ImageSearchResultPage(browser)
    
    with allure.step(f'Выбор {search_result_num}й картинки из результатов поиска'):
        first_search_result_url = images_search_result_page.get_search_result_url(search_result_num)
        images_search_result_page.select_search_result(search_result_num)
    
    images_swipe_modal_window = ImageSwipeModalWindow(browser)
    
    with allure.step('Проверка что открылось модалка со слайдером изображений'):
        assert images_swipe_modal_window.modal_window, 'не открылось окно со слайдером изображений'
    
    with allure.step('Проверка что в слайдере открылось изображение'):
        assert images_swipe_modal_window.swipe_preview, 'не открылось изображение в слайдере'
    with allure.step('Проверка что открылось именно выбранное изображение'):
        swipe_preview_url = images_swipe_modal_window.get_swipe_preview_url()
        assert first_search_result_url in swipe_preview_url, 'открылось неверное изображение'
    
    with allure.step('Нажать кнопку "следующее изображение" на слайдере'):
        images_swipe_modal_window.next_button_click()
    
    with allure.step('Проверка что в слайдере открылось изображение'):
        assert images_swipe_modal_window.swipe_preview, 'не открылось изображение в слайдере'
    with allure.step('Проверка что изображение новое (сменилось)'):
        swipe_preview_url = images_swipe_modal_window.get_swipe_preview_url()
        assert swipe_preview_url not in first_search_result_url, 'изображение не сменилось'
    
    with allure.step('Нажать кнопку "предыдущее изображение" на слайдере'):
        images_swipe_modal_window.prev_button_click()
    
    with allure.step('Проверка что в слайдере открылось изображение'):
        assert images_swipe_modal_window.swipe_preview, 'не открылось изображение в слайдере'
    with allure.step('Проверка что изображение сменилось на первое'):
        swipe_preview_url = images_swipe_modal_window.get_swipe_preview_url()
        assert first_search_result_url in swipe_preview_url, 'открылось неверное изображение'
    
    images_swipe_modal_window.close_button.click()
    
    logging.info('конец теста "поиск в Яндекс-Картинках"')
    
    time.sleep(3)
