import pytest
import allure
from datetime import datetime
import os


@pytest.fixture(scope="session", autouse=True)
def setup_allure():
    """Настройка Allure окружения"""
    os.makedirs("allure-results", exist_ok=True)
    
    env_file = "allure-results/environment.properties"
    with open(env_file, "w") as f:
        f.write(f"BASE_URL=https://qa-scooter.praktikum-services.ru\n")
        f.write(f"TestRun={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tester=QA Engineer\n")
        f.write(f"Project=QA Sprint 7\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для получения результатов тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    # Добавляем описание теста в отчет
    if rep.when == "call":
        # Получаем docstring теста
        if item._obj.__doc__:
            allure.dynamic.description(item._obj.__doc__)
        
        # Устанавливаем заголовок из allure.title или из имени теста
        title = item.name.replace("_", " ").title()
        # Проверяем, есть ли у теста декоратор allure.title
        if hasattr(item.function, '__allure_title__'):
            title = item.function.__allure_title__
        allure.dynamic.title(title)
        
        # Добавляем теги
        for marker in item.iter_markers():
            allure.dynamic.tag(marker.name)