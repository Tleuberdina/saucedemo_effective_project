"""
Файл для создания WebDriver в Docker окружении.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


def get_docker_driver():
    """
    Создает и возвращает WebDriver для Docker.
    """
    chrome_options = Options()
    
    # Настройки для Docker
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Дополнительные настройки
    chrome_options.add_argument("--disable-extensions")
    
    # Ищем chromedriver
    if os.path.exists('/usr/local/bin/chromedriver'):
        chromedriver_path = '/usr/local/bin/chromedriver'
    elif os.path.exists('/usr/bin/chromedriver'):
        chromedriver_path = '/usr/bin/chromedriver'
    else:
        chromedriver_path = 'chromedriver'
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Таймауты
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    return driver
