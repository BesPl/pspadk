import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType

class BasePage:
    PAGE_URL = None  # Должен быть переопределен в дочерних классах

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = self._setup_logger()


    def _wait_element(self, by: By, value: str, timeout=None) -> WebElement:
        if timeout is None:
            timeout = self.timeout
        return self.wait.until(
            EC.element_to_be_clickable((by, value)),
            message=f"Элемент {value} не найден за {timeout} секунд"
        )

    def open(self):
        with allure.step(f"Open {self.PAGE_URL} page"):
            self.driver.get(self.PAGE_URL)
            self.logger.info(f"Открыта страница: {self.PAGE_URL}")

    def is_opened(self, timeout=10):
        with allure.step(f"Check if {self.PAGE_URL} is opened"):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.url_to_be(self.PAGE_URL)
                )
                self.logger.info(f"Страница {self.PAGE_URL} открыта")
                return True
            except TimeoutException:
                self.logger.error(f"Страница {self.PAGE_URL} не открылась")
                return False

    def make_screenshot(self, screenshot_name):
        try:
            allure.attach(
                body=self.driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=AttachmentType.PNG
            )
            self.logger.info(f"Скриншот {screenshot_name} добавлен")
        except Exception as e:
            self.logger.error(f"Ошибка создания скриншота: {str(e)}")
            raise

    def click_element(self, by: By, value: str, timeout=None):
        try:
            element = self._wait_element(by, value, timeout)
            element.click()
            self.logger.info(f"Нажата кнопка {value}")
        except Exception as e:
            self.logger.error(f"Не удалось нажать на элемент {value}: {str(e)}")
            raise

    def input_text(self, by: By, value: str, text: str, timeout=None):
        try:
            element = self._wait_element(by, value, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"В поле {value} введён текст: {text}")
        except Exception as e:
            self.logger.error(f"Ошибка ввода текста в элемент {value}: {str(e)}")
            raise

    def get_element_text(self, by: By, value: str, timeout=None) -> str:
        try:
            element = self._wait_element(by, value, timeout)
            text = element.text
            self.logger.info(f"Текст элемента {value}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Ошибка получения текста элемента {value}: {str(e)}")
            raise

    def is_element_enabled(self, by: By, value: str, timeout=None) -> bool:
        try:
            element = self._wait_element(by, value, timeout)
            is_enabled = element.is_enabled()
            self.logger.info(f"Элемент {value} доступен для клика: {is_enabled}")
            return is_enabled
        except Exception as e:
            self.logger.error(f"Ошибка проверки элемента {value}: {str(e)}")
            raise

    def get_current_url(self) -> str:
        current_url = self.driver.current_url
        self.logger.info(f"Текущий URL: {current_url}")
        return current_url

    def scroll_to_element(self, by: By, value: str, timeout=None):
        try:
            element = self._wait_element(by, value, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.logger.info(f"Скролл до элемента {value} выполнен")
        except Exception as e:
            self.logger.error(f"Ошибка скролла до элемента {value}: {str(e)}")
            raise

    def js_click(self, by: By, value: str):
        element = self._wait_element(by, value)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"JS-клик по элементу {value}")

    def is_element_present(self, by: By, value: str, timeout=None) -> bool:
        try:
            self._wait_element(by, value, timeout)
            return True
        except TimeoutException:
            return False

    def check_current_url(self, expected_url):
        current_url = self.get_current_url()
        assert current_url == expected_url, (
            f"Ожидался URL: {expected_url}, "
            f"получен: {current_url}"
        )