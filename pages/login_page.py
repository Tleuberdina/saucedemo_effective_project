from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    """
    Page Object для страницы логина SauceDemo
    URL: https://www.saucedemo.com/.
    """
    
    # Локаторы элементов
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    INVENTORY_CONTAINER = (By.ID, 'inventory_container')
    APP_LOGO = (By.CLASS_NAME, 'app_logo')
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        """Открывает страницу логина."""
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def enter_username(self, username):
        """Вводит имя пользователя."""
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        return self
    
    def enter_password(self, password):
        """Вводит пароль."""
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self
    
    def click_login(self):
        """Нажимает кнопку Login."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self
    
    def get_error_text(self):
        """Возвращает текст ошибки."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
        except TimeoutException:
            return ""
    
    def get_current_url(self):
        """Возвращает текущий URL."""
        return self.driver.current_url
    
    def is_inventory_page_loaded(self, timeout=10):
        """
        Проверяет, загрузилась ли страница каталога после успешного входа
        
        Args:
            timeout (int): Время ожидания в секундах
            
        Returns:
            bool: True если страница загружена, иначе False.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Проверяем URL
            wait.until(EC.url_contains("/inventory.html"))
            # Проверяем видимость контейнера с товарами
            wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))
            # Проверяем видимость логотипа
            wait.until(EC.visibility_of_element_located(self.APP_LOGO))
            return True
        except TimeoutException:
            return False
    
    def login(self, username, password):
        """Выполняет полный процесс входа."""
        return self.open().enter_username(username).enter_password(password).click_login()
    
    def clear_fields(self):
        """Очищает поля ввода."""
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        return self
