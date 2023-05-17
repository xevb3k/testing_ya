import time
from pages.main_page import MainPage
from pages.search_result_page import SearchResultPage
from pages.image_search_page import ImageSearchPage
from pages.image_search_result_page import ImageSearchResultPage
from pages.images_swipe_page import ImageSwipeModalWindow
from selenium.webdriver import Keys
import pytest
import allure
import logging

search_request = 'тензор'
valid_url = 'https://tensor.ru/'
valid_url2 = 'https://yandex.ru/images/'
test_data_1 = [(search_request, valid_url, 0)]


@allure.title('Поиск в Яндекс')
@allure.feature('search')
@allure.feature('suggest list')
@allure.feature('serp')
@allure.description(f'Поиск по "{search_request}", проверка что выпадает таблица с подсказками поиска, '
                    f'проверка что 1я ссылка ведет на {valid_url}')
@pytest.mark.headless_mode(False)
@pytest.mark.parametrize("test_input, expected, link_number", test_data_1, ids=['test_set_1'])
def test_search(firefox_browser, test_input, expected, link_number):
    logging.info('тест "поиск в Яндексе"')

    browser = firefox_browser

    with allure.step(f'Открыть страницу'):
        main_page = MainPage(browser)
        main_page.open_main_page()
    
    with allure.step('Проверка наличия поля поиска'):
        assert main_page.search_field_new, 'не найдено поле поиска'

    with allure.step(f'Ввод поискового запроса "{test_input}"'):
        main_page.search_field_new = test_input
        
    with allure.step('Проверка наличия всплывающей таблицы с подсказками'):
        assert main_page.suggest_search_prompt_list, 'нет всплывающей таблицы с подсказками'

    with allure.step('Переход к результатам поиска'):
        main_page.search_field_new = Keys.ENTER

    search_result_page = SearchResultPage(browser)

    with allure.step('Проверка наличия поисковой выдачи'):
        assert search_result_page.search_result_container, 'отсутствует поисковая выдача'

    with allure.step(f'Проверка, что URL {link_number}-го результата {expected}'):
        first_search_result = search_result_page.search_result_elements[link_number]
        url = search_result_page.get_search_result_link(first_search_result)
        assert url in expected, f'первая ссылка в результатах поиска не ведет на {expected}'

    # необязательный шаг
    with allure.step(f'Проверка, что при клике на {link_number}й результат поиска переходим на {valid_url}'):
        new_url = main_page.goto_link(search_result_page.search_result_elements[link_number])
        assert valid_url in new_url, f'не происходит переход на {valid_url}'

    logging.info('конец теста "поиск в Яндексе"')
    

@allure.title('Поиск в Яндекс-Картинках')
@allure.feature('suggest menu')
@allure.feature('main menu')
@allure.feature('image search')
@allure.feature('image view')
@allure.feature('image swipe')
@allure.description('Переход со страницы ya.ru на ya.ru/images через suggest->main menu, поиск картинок из первой '
                    'популярной категории, просмотр первой картинки из результатов поиска, листание картинок')
@pytest.mark.headless_mode(False)
@pytest.mark.parametrize("category_num, search_result_num", [(0, 0)])
def test_images(firefox_browser, category_num, search_result_num):
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

    with allure.step(f'Проверка что произошел переход на {valid_url2} при клике на кнопку "Картинки"'):
        url = main_page.main_menu_images_button_click()
        assert url in valid_url2, f'не произошел переход на {valid_url2}'
    
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
