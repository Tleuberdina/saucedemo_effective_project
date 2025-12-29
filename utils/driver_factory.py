import sys
import platform
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class DriverFactory:
    """Фабрика для создания и настройки экземпляра WebDriver."""

    @staticmethod
    def get_driver(headless=False):
        """
        Создает и возвращает настроенный экземпляр Chrome WebDriver.
        """
        # Проверяем, находимся ли мы в Docker
        in_docker = os.path.exists('/.dockerenv')

        chrome_options = Options()

        # Обязательные опции для стабильности в Docker/CI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Headless режим (всегда в Docker, или если указано)
        if headless or in_docker:
            chrome_options.add_argument("--headless=new") # Используем новый headless режим
            chrome_options.add_argument("--window-size=1920,1080")

        # Дополнительные настройки для отключения автоматизационных флагов
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            # Ключевое изменение: указываем путь к бинарнику Chrome и позволяем Selenium управлять драйвером
            # В Docker Chrome установлен в /usr/bin/google-chrome
            service = Service(executable_path='/usr/bin/google-chrome')

            # Создаем драйвер. Selenium 4.6+ автоматически скачает и использует
            # ПРАВИЛЬНУЮ версию ChromeDriver через Selenium Manager.
            driver = webdriver.Chrome(service=service, options=chrome_options)

        except Exception as e:
            print(f"❌ Ошибка при создании драйвера: {e}")
            print("🔄 Пытаемся использовать fallback-стратегию...")

            # Fallback: пробуем без указания пути к сервису
            try:
                driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                print(f"❌ Fallback также не сработал: {e2}")
                raise

        # Настройки таймаутов
        driver.implicitly_wait(10)  # Увеличиваем для стабильности
        driver.set_page_load_timeout(30)

        return driver

    @staticmethod
    def get_headless_driver():
        """Алиас для получения headless драйвера."""
        return DriverFactory.get_driver(headless=True)
