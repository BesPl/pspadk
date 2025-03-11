import pytest
import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver():
    """Фикстура для инициализации WebDriver с Selenium Grid в Docker."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Указываем URL Selenium Grid из Docker Compose
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=chrome_options
    )

    yield driver
    driver.quit()


@pytest.fixture
def username():
    """Возвращает имя пользователя из .env."""
    return os.getenv("USERNAME")


@pytest.fixture
def password():
    """Возвращает пароль из .env."""
    return os.getenv("PASSWORD")


@pytest.fixture
def api_token():
    """Возвращает API-токен из .env."""
    return os.getenv("API_TOKEN")


@pytest.fixture
def base_url():
    """Базовый URL для UI-тестов."""
    return "https://demoqa.com"


@pytest.fixture
def api_base_url():
    """Базовый URL для API-тестов."""
    return "https://api.demoqa.com"


@pytest.fixture
def wait(driver):
    """Фикстура для ожидания элементов (WebDriverWait)."""
    return WebDriverWait(driver, timeout=10)


@pytest.fixture
def logger():
    """Фикстура для логгера."""
    return logging.getLogger(__name__)


@pytest.fixture
def enable_allure_screenshot(driver):
    """Автоматически добавляет скриншот при провале теста в Allure."""
    yield
    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )