Этот репозиторий содержит автотесты сайта https://ya.ru/.

Тесты выполнены на Python 3.9 с применением PageObject и фреймворков pytest/selenium.
Логирование через logger, отчетность allure.

Тесты запускаются в браузере Mozilla Firefox и Google Chrome (предпочтительнее Firefox, так как Chrome часто выдает капчу).

Возможен запуск в headless-режиме.

Установка зависимостей: pip install -r requirements

Запуск локально:
python -m pytest -v [<test_file_name>[::<test_name>]]

Запуск с allure reports:
python -m pytest --alluredir=test_results [<test_file_name>[::<test_name>]]

Просмотр отчета:
allure serve test_results
