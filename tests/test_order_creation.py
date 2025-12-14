import pytest
import allure
from unittest.mock import Mock
from api_clients.order_api import OrderAPI
from data.test_data import CourierData
from api_mocks.order_creation_mocks import OrderMocks


@allure.feature("Создание заказа")
@allure.story("API: POST /api/v1/orders - создание заказа с разными цветами")
class TestOrderCreation:

    @pytest.fixture
    def basic_order_data(self):
        """Фикстура с базовыми данными для заказа"""
        return CourierData.create_order_data()

    @pytest.fixture
    def mock_session_success(self):
        """Фикстура: мок для успешного создания заказа"""
        return OrderMocks.create_mock_session_for_order_creation(
            status_code=201,
            track_number=123456
        )

    @pytest.mark.parametrize("color_data,test_description", [
        (["BLACK"], "Создание заказа с цветом BLACK"),
        (["GREY"], "Создание заказа с цветом GREY"),
        (["BLACK", "GREY"], "Создание заказа с обоими цветами"),
        ([], "Создание заказа без указания цвета (пустой массив)"),
    ])
    @allure.title("Тест: Создание заказа - проверка кода ответа 201")
    def test_create_order_status_code_201(
        self, basic_order_data, mock_session_success, color_data, test_description
    ):
        """
        Тест с параметризацией по 4 вариантам цвета.
        Проверяем, что создание заказа возвращает код 201.
        """
        order_data = {**basic_order_data, "color": color_data}
        api = OrderAPI(session=mock_session_success)
        response = api.create_order(order_data)

        assert response.status_code == 201

    @pytest.mark.parametrize("color_data,test_description", [
        (["BLACK"], "Создание заказа с цветом BLACK"),
        (["GREY"], "Создание заказа с цветом GREY"),
        (["BLACK", "GREY"], "Создание заказа с обоими цветами"),
        ([], "Создание заказа без указания цвета (пустой массив)"),
    ])
    @allure.title("Тест: Создание заказа - проверка наличия track в теле ответа")
    def test_create_order_returns_track(
        self, basic_order_data, mock_session_success, color_data, test_description
    ):
        """
        Тест с параметризацией по 4 вариантам цвета.
        Проверяем, что тело ответа содержит track.
        """
        order_data = {**basic_order_data, "color": color_data}
        api = OrderAPI(session=mock_session_success)
        response = api.create_order(order_data)

        response_json = response.json()
        assert "track" in response_json