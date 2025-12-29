import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory


@allure.suite("Тесты авторизации SauceDemo.")
class TestLogin:
    """Набор тестов для проверки авторизации на сайте SauceDemo."""
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """
        Фикстура для инициализации и завершения работы драйвера.
        """
        # Определяем, нужно ли запускать в headless режиме
        headless = request.config.getoption("--headless", default=False)
        self.driver = DriverFactory.get_driver(headless=headless)
        self.login_page = LoginPage(self.driver)
        
        # Завершаем работу после теста
        yield
        if self.driver:
            self.driver.quit()
    
    @allure.title("1. Успешный логин стандартным пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
    Тест проверяет успешную авторизацию с валидными учетными данными.
    Ожидается:
    1. Переход на страницу /inventory.html
    2. Отображение контейнера с товарами
    3. Отображение логотипа приложения.
    """)
    def test_successful_login(self):
        with allure.step("Открыть страницу логина."):
            self.login_page.open()
        
        with allure.step("Ввести валидные учетные данные"):
            self.login_page.enter_username("standard_user")
            self.login_page.enter_password("secret_sauce")
        
        with allure.step("Нажать кнопку Login"):
            self.login_page.click_login()
        
        with allure.step("Проверить успешный вход"):
            # Проверяем URL
            current_url = self.login_page.get_current_url()
            assert "/inventory.html" in current_url, \
                f"Ожидался URL содержащий '/inventory.html', получен: {current_url}"
            
            # Проверяем загрузку страницы
            assert self.login_page.is_inventory_page_loaded(), \
                "Страница каталога не загрузилась после успешного входа"
            
        with allure.step("Сделать скриншот успешного входа"):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="successful_login_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.title("2. Логин с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет поведение системы при вводе неверного пароля.
    Ожидается сообщение об ошибке.
    """)
    def test_invalid_password(self):
        with allure.step("Выполнить вход с неверным паролем"):
            self.login_page.login("standard_user", "wrong_password")
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = self.login_page.get_error_text()
            assert error_text != "", "Сообщение об ошибке не отображается"
            assert "Username and password do not match" in error_text, \
                f"Неверное сообщение об ошибке: {error_text}"
            
        with allure.step("Проверить, что остались на странице логина"):
            current_url = self.login_page.get_current_url()
            assert current_url == "https://www.saucedemo.com/", \
                f"Ожидался URL страницы логина, получен: {current_url}"
    
    @allure.title("3. Логин заблокированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_locked_out_user(self):
        with allure.step("Выполнить вход заблокированным пользователем"):
            self.login_page.login("locked_out_user", "secret_sauce")
        
        with allure.step("Проверить сообщение об ошибке блокировки"):
            error_text = self.login_page.get_error_text()
            assert "Sorry, this user has been locked out" in error_text, \
                f"Неверное сообщение об ошибке для заблокированного пользователя: {error_text}"
    
    @allure.title("4. Логин с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_credentials(self):
        with allure.step("Попытаться войти без ввода данных"):
            self.login_page.open().click_login()
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = self.login_page.get_error_text()
            assert "Username is required" in error_text, \
                f"Ожидалось сообщение 'Username is required', получено: {error_text}"
    
    @allure.title("5. Логин пользователем performance_glitch_user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Тест проверяет вход пользователем, для которого возможны задержки.
    Ожидается успешный вход, несмотря на возможные задержки.
    """)
    def test_performance_glitch_user(self):
        with allure.step("Выполнить вход пользователем performance_glitch_user"):
            self.login_page.login("performance_glitch_user", "secret_sauce")
        
        with allure.step("Проверить успешный вход с увеличенным таймаутом"):
            # Увеличиваем ожидание для пользователя с возможными задержками
            assert self.login_page.is_inventory_page_loaded(timeout=15), \
                "Страница не загрузилась в течение 15 секунд для пользователя performance_glitch_user"
            
            current_url = self.login_page.get_current_url()
            assert "/inventory.html" in current_url, \
                f"Ожидался URL содержащий '/inventory.html', получен: {current_url}"


# Хуки для добавления скриншотов при падении тестов
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Получаем драйвер из теста
        for fixturename in item.fixturenames:
            if "driver" in fixturename:
                driver = item.funcargs[fixturename]
                break
        else:
            return
        
        # Делаем скриншот
        screenshot = driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )
