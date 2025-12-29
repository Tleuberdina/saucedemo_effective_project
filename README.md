# Автоматизация тестирования логина SauceDemo
## Описание:
Проект для автоматизации тестирования функциональности авторизации на сайте https://www.saucedemo.com/.

### Технологии:
- Язык программирования — Python 3.10
- Автоматизация браузера — Selenium WebDriver
- Фреймворк для тестирования — Pytest
- Создание отчетов — Allure
- Контейнеризация — Docker
- Паттерн проектирования - Page Object Pattern

### Установка и запуск
1. Клонировать репозиторий и перейти в него в командной строке:
   #### git clone git@github.com:Tleuberdina/saucedemo_effective_project.git
   #### cd saucedemo_effective_project
3. Cоздать и активировать виртуальное окружение:
   #### python -m venv venv
   #### source venv/Scripts/activate
4. Установить зависимости из файла requirements.txt:
   #### python -m pip install -- upgrade pip
   #### pip install -r requirements.txt
5. Запустить тесты локально:
   #### pytest tests/
6. Запустить тесты локально с генерацией отчета Allure:
   #### pytest tests/ --alluredir=allure-results
7. Локально просмотр отчетов Allure в браузере (после запуска тестов с флагом --alluredir):
   #### allure serve allure-results
8. Локально сгенерировать статический HTML отчет Allure (после запуска тестов с флагом --alluredir):
   #### allure generate allure-results -o allure-report
9. Скриншоты:
   #### при падении тестов автоматически создаются скриншоты, которые прикрепляются к отчетам Allure.
10. Запуск в Docker (собираем образ, запускаем тесты в контейнере):
   #### docker build -t sauce-demo-tests .
   #### docker run --rm sauce-demo-tests
11. Запуск тестов в Docker с генерацией отчета Allure:
   #### docker run --rm -v allure-results:/app/allure-results saucedemo-tests
12. В Docker сгенерировать статический HTML отчет Allure (после запуска тестов с allure-results):
   #### docker run --rm -v ${PWD}/allure-results:/allure-results -v ${PWD}/allure-report:/allure-report frankescobar/allure-docker-service allure generate /allure-results -o /allure-report --clean
13. В Docker открыть отчет (после запуска тестов с allure-results):
   #### start allure-report/index.html
