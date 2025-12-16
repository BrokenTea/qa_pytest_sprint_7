import pytest
import allure
from unittest.mock import Mock
from datetime import datetime
import os
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData
from data.unique_data_generator import UniqueDataGenerator
from api_mocks.courier_creation_mocks import CourierMocks
from api_mocks.courier_login_mocks import CourierLoginMocks
from api_mocks.order_creation_mocks import OrderMocks


# === НАСТРОЙКА ALLURE ===
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


# === ФИКСТУРЫ ДЛЯ КУРЬЕРОВ ===
@pytest.fixture
def delete_courier():
    """Фикстура для удаления курьера"""
    courier_ids = []
    courier_api = CourierAPI()
    
    def _delete(courier_id):
        if courier_id:
            courier_ids.append(courier_id)
    
    yield _delete
    
    for courier_id in courier_ids:
        courier_api.delete_courier(courier_id)


# === ФИКСТУРЫ ТЕСТОВЫХ ДАННЫХ (РАЗДЕЛЕНИЕ ПО ФУНКЦИОНАЛЬНОСТИ) ===

# Данные для создания курьера
@pytest.fixture
def unique_courier_data():
    """Фикстура с уникальными данными для каждого теста"""
    return UniqueDataGenerator.generate_unique_courier_data()


@pytest.fixture
def courier_data():
    """Фикстура с тестовыми данными (старая версия для обратной совместимости)"""
    return CourierData.get_valid_courier_data()


@pytest.fixture
def random_login_data():
    """Фикстура со случайными тестовыми данными для логина"""
    return CourierData.get_valid_courier_data()


@pytest.fixture
def basic_order_data():
    """Фикстура с базовыми данными для заказа"""
    return CourierData.create_order_data()


# === МОКИ ДЛЯ СОЗДАНИЯ КУРЬЕРА ===
@pytest.fixture
def mock_courier_session_error():
    """Фикстура: мок для ошибки при создании курьера"""
    return CourierMocks.create_mock_session(
        post_status_code=CourierData.API_ERROR_CODES["BAD_REQUEST"],
        post_json_data={
            "message": CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_ACCOUNT_CREATION"],
            "code": CourierData.API_ERROR_CODES["BAD_REQUEST"]
        }
    )


@pytest.fixture
def mock_courier_session_conflict():
    """Фикстура: мок для конфликта при создании курьера (код 409)"""
    mock_session = Mock()
    mock_response = CourierMocks.create_mock_response(
        status_code=CourierData.API_ERROR_CODES["CONFLICT"],
        json_data=CourierMocks.get_duplicate_error_response()
    )
    mock_session.post.return_value = mock_response
    return mock_session


# === МОКИ ДЛЯ ЛОГИНА КУРЬЕРА ===
@pytest.fixture
def mock_session_login_success():
    """Фикстура: мок для успешного логина"""
    return CourierLoginMocks.create_success_mock_session()


@pytest.fixture
def mock_session_login_missing_data():
    """Фикстура: мок для ошибки недостатка данных (400)"""
    return CourierLoginMocks.create_missing_data_mock_session()


@pytest.fixture
def mock_session_login_not_found():
    """Фикстура: мок для ошибки не найденной учетной записи (404)"""
    return CourierLoginMocks.create_not_found_mock_session()


# === МОКИ ДЛЯ СОЗДАНИЯ ЗАКАЗА ===
@pytest.fixture
def mock_order_session_success():
    """Фикстура: мок для успешного создания заказа"""
    return OrderMocks.create_success_mock_session()


# === МОКИ ДЛЯ СПИСКА ЗАКАЗОВ (ОСТАВЛЯЕМ ТОЛЬКО БАЗОВУЮ ФИКСТУРУ) ===
@pytest.fixture
def mock_order_list_basic():
    """Фикстура: мок для базового получения списка заказов"""
    from api_mocks.order_list_mocks import OrderListMocks
    return OrderListMocks.create_basic_mock_session()