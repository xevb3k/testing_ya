import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import random
import logging


@pytest.fixture()
def firefox_browser(request):
    """
    Настраивает драйвер FireFox
    :param request: headless_mode = True для безголового режима
    :return: драйвер
    """
    logging.info('настройка Firefox')
    headless = request.node.get_closest_marker("headless_mode").args[0]
    fox_options = webdriver.FirefoxOptions()
    if headless:
        logging.info('headless режим Firefox')
        fox_options.add_argument('--headless')
    fox_options.add_argument('-width=1920')
    fox_options.add_argument('-height=1080')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=fox_options)
    driver.set_window_position(0, 0)
    try:
        logging.info('переход к тесту')
        yield driver
    finally:
        logging.info('закрытие драйвера Firefox')
        driver.quit()


# на тестируемом сайте ya.ru при работе через ChromeDriver в 50% показывают капчу, просьба пользоваться FireFox
@pytest.fixture()
def chrome_browser(request):
    """
    Настраивает драйвер Chrome
    :param request: headless_mode = True для безголового режима
    :return: драйвер
    """
    logging.info('настройка Chrome')
    headless = request.node.get_closest_marker("headless_mode").args[0]
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    
    # антикапча
    x = random.randint(1280, 1820)
    y = random.randint(720, 980)
    chrome_options.add_argument(f"--window-size={x},{y}")
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    chrome_options.add_argument(f"--window-position={x},{y}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    if headless:
        logging.info('headless режим Chrome')
        chrome_options.add_argument("--headless=new")

    logging.info('запуск драйвера Chrome')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    try:
        logging.info('переход к тесту')
        yield driver
    finally:
        logging.info('закрытие драйвера Chrome')
        driver.quit()
