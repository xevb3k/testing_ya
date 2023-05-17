from pages.main_page import MainPage
from pages.search_result_page import SearchResultPage
from selenium.webdriver import Keys
import time
import pytest
import allure
import logging

search_request = 'тензор'
valid_url = 'https://tensor.ru/'

# test_input, expected, link_number
test_data_1 = [(search_request, valid_url, 0)]


@allure.title('Поиск в Яндекс')
@allure.feature('search')
@allure.feature('suggest list')
@allure.feature('serp')
@allure.description(f'Поиск по "test_input", проверка что выпадает таблица с подсказками поиска, '
                    f'проверка что "link_number" ссылка ведет на "expected"')
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
    with allure.step(f'Проверка, что при клике на {link_number}й результат поиска переходим на {expected}'):
        new_url = main_page.goto_link(search_result_page.search_result_elements[link_number])
        assert expected in new_url, f'не происходит переход на {expected}'

    logging.info('конец теста "поиск в Яндексе"')
    
    # исключительно для демонстрации
    time.sleep(3)
    