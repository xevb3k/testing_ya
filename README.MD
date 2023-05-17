Этот репозиторий содержит автотесты сайта https://ya.ru/.
Тесты выполнены на Python 3.9 с применением PageObject и фреймворков pytest/selenium.
Тесты запускаются в браузере Google Chrome и/или Mozilla Firefox. 

Установка зависимостей: pip3 install -r requirements

Запуск локально:
python -m pytest -v [<test_file_name>[::<test_name>]]

Запуск с allure reports:
python -m pytest --alluredir=test_results [<test_file_name>[::<test_name>]]

Просмотр отчета:
allure serve test_results

