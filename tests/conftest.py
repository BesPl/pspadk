import pytest
import logging
import allure
import json
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Инициализация логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_config():
    """Загрузка конфигурации из файла config.json с проверкой обязательных полей"""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            # Проверка обязательных полей
            required_fields = ["BROWSER", "HEADLESS"]
            for field in required_fields:
                if field not in config:
                    logger.warning(
                        f"Отсутствует обязательное поле {field} в config.json, используется значение по умолчанию")
                    config[field] = {"BROWSER": "chrome", "HEADLESS": True}[field]
            return config
    except FileNotFoundError:
        logger.error("Файл config.json не найден. Используются настройки по умолчанию")
        return {"BROWSER": "chrome", "HEADLESS": True}
    except json.JSONDecodeError:
        logger.error("Ошибка декодирования файла config.json. Используются настройки по умолчанию")
        return {"BROWSER": "chrome", "HEADLESS": True}

@pytest.fixture(scope="session")
def browser():
    """Фикстура для инициализации WebDriver с настройками из config.json"""
    config = load_config()

    # Логирование настроек
    logger.info(f"Настройки браузера: BROWSER={config['BROWSER']}, HEADLESS={config['HEADLESS']}")

    browser_name = config["BROWSER"].lower()
    headless = config["HEADLESS"]

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if headless:
        options.add_argument("--headless=new")

    if browser_name == "firefox":
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        driver = webdriver.Edge(options=options)
    else:
        logger.info("Используется Chrome по умолчанию")
        driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    yield driver

    logger.info(f"Закрытие браузера {browser_name}")
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def setup(request, browser):
    """Фикстура для подготовки тестового окружения с улучшенной обработкой"""
    # Очистка куки перед тестом
    browser.delete_all_cookies()

    # Получение имени теста через pytest item
    test_name = request.node.name if hasattr(request, "node") else "Unknown"
    logger.info(f"Начало теста: {test_name}")

    yield

    logger.info(f"Завершение теста: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Обработчик для сохранения скриншотов при падении теста с улучшенной обработкой"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Извлечение драйвера через фикстуру
        driver = item.funcargs.get("browser", None)

        if driver:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"failure_{item.name}_{timestamp}.png"
            screenshots_dir = "screenshots"

            # Создание структуры папок по датам
            today_dir = datetime.datetime.now().strftime("%Y-%m-%d")
            full_path = os.path.join(screenshots_dir, today_dir)
            os.makedirs(full_path, exist_ok=True)

            try:
                driver.save_screenshot(os.path.join(full_path, screenshot_name))
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.error(f"Ошибка сохранения скриншота: {str(e)}")
        else:
            logger.warning("Драйвер не найден для сохранения скриншота")

@pytest.fixture
def base_url():
    """Базовый URL для UI-тестов с проверкой переменных окружения"""
    url = os.getenv("BASE_URL")
    if not url:
        logger.warning("Переменная окружения BASE_URL не установлена. Используется значение по умолчанию")
        url = "https://demoqa.com"
    return url

@pytest.fixture
def api_base_url():
    """Базовый URL для API-тестов с проверкой переменных окружения"""
    url = os.getenv("API_URL")
    if not url:
        logger.warning("Переменная окружения API_URL не установлена. Используется значение по умолчанию")
        url = "https://api.demoqa.com"
    return url

@pytest.fixture
def auth_token():
    """Получение токена авторизации с проверкой"""
    token = os.getenv("API_TOKEN", "default_token")
    if token == "default_token":
        logger.warning("API_TOKEN не задан в переменных окружения. Используется тестовый токен")
    return token