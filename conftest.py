import pytest
import allure
from unittest.mock import Mock
from datetime import datetime
import os
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData
from api_mocks.courier_creation_mocks import CourierMocks
from api_mocks.courier_login_mocks import CourierLoginMocks
from api_mocks.order_creation_mocks import OrderMocks
from data.data_factory import DataFactory

# Конфигурация Allure для генерации отчетов
@pytest.fixture(scope="session", autouse=True)
def setup_allure():
    os.makedirs("allure-results", exist_ok=True)
    
    env_file = "allure-results/environment.properties"
    with open(env_file, "w") as f:
        f.write(f"BASE_URL=https://qa-scooter.praktikum-services.ru\n")
        f.write(f"TestRun={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tester=QA Engineer\n")
        f.write(f"Project=QA Sprint 7\n")

# Хук для динамического добавления информации в Allure отчет
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        # Добавляем описание теста из docstring
        if item._obj.__doc__:
            allure.dynamic.description(item._obj.__doc__)
        
        # Устанавливаем заголовок теста
        title = item.name.replace("_", " ").title()
        if hasattr(item.function, '__allure_title__'):
            title = item.function.__allure_title__
        allure.dynamic.title(title)
        
        # Добавляем маркеры как теги
        for marker in item.iter_markers():
            allure.dynamic.tag(marker.name)

# Фикстура для очистки тестовых данных после тестов
@pytest.fixture
def delete_courier():
    courier_ids = []
    courier_api = CourierAPI()
    
    def _delete(courier_id):
        if courier_id:
            courier_ids.append(courier_id)  # Собираем ID для удаления после теста
    
    yield _delete  # Возвращаем функцию удаления
    
    # Удаляем всех созданных курьеров после завершения теста
    for courier_id in courier_ids:
        courier_api.delete_courier(courier_id)

# Фикстуры тестовых данных
@pytest.fixture
def unique_courier_data():
    """Уникальные данные курьера для каждого теста"""
    return DataFactory.get_unique_courier_data()

@pytest.fixture
def courier_data():
    """Стандартные тестовые данные курьера"""
    return DataFactory.get_valid_courier_data()

@pytest.fixture
def random_login_data():
    """Случайные данные для логина"""
    return DataFactory.get_valid_courier_data()

@pytest.fixture
def basic_order_data():
    """Базовые данные для создания заказа"""
    return DataFactory.create_order_data()

# Моки для создания курьера
@pytest.fixture
def mock_courier_session_error():
    """Мок для симуляции ошибки 400 при создании курьера"""
    return CourierMocks.create_mock_session(
        post_status_code=CourierData.API_ERROR_CODES["BAD_REQUEST"],
        post_json_data={
            "message": CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_ACCOUNT_CREATION"],
            "code": CourierData.API_ERROR_CODES["BAD_REQUEST"]
        }
    )

@pytest.fixture
def mock_courier_session_conflict():
    """Мок для симуляции конфликта 409 (дубликат логина)"""
    mock_session = Mock()
    mock_response = CourierMocks.create_mock_response(
        status_code=CourierData.API_ERROR_CODES["CONFLICT"],
        json_data=CourierMocks.get_duplicate_error_response()
    )
    mock_session.post.return_value = mock_response
    return mock_session

# Моки для логина курьера
@pytest.fixture
def mock_session_login_success():
    """Мок для успешного логина (200)"""
    return CourierLoginMocks.create_success_mock_session()

@pytest.fixture
def mock_session_login_missing_data():
    """Мок для ошибки недостатка данных при логине (400)"""
    return CourierLoginMocks.create_missing_data_mock_session()

@pytest.fixture
def mock_session_login_not_found():
    """Мок для ошибки 'учетная запись не найдена' (404)"""
    return CourierLoginMocks.create_not_found_mock_session()

# Моки для создания заказа
@pytest.fixture
def mock_order_session_success():
    """Мок для успешного создания заказа (201)"""
    return OrderMocks.create_success_mock_session()

# Моки для получения списка заказов
@pytest.fixture
def mock_order_list_basic():
    """Мок для базового получения списка заказов"""
    from api_mocks.order_list_mocks import OrderListMocks
    return OrderListMocks.create_basic_mock_session()