import pytest
import allure
from api_clients.order_api import OrderAPI
from data.test_data import CourierData


@allure.feature("Создание заказа")
@allure.story("API: POST /api/v1/orders - создание заказа с разными цветами")
class TestOrderCreation:

    @pytest.mark.parametrize("color_data,test_description", [
        (["BLACK"], "Создание заказа с цветом BLACK"),
        (["GREY"], "Создание заказа с цветом GREY"),
        (["BLACK", "GREY"], "Создание заказа с обоими цветами"),
        ([], "Создание заказа без указания цвета (пустой массив)"),
    ])
    @allure.title("Тест: Создание заказа - проверка кода ответа 201")
    def test_create_order_status_code_201(
        self, basic_order_data, mock_order_session_success, color_data, test_description
    ):
        """
        Тест с параметризацией по 4 вариантам цвета.
        Проверяем, что создание заказа возвращает код 201.
        """
        order_data = {**basic_order_data, "color": color_data}
        api = OrderAPI(session=mock_order_session_success)
        response = api.create_order(order_data)

        assert response.status_code == CourierData.API_ERROR_CODES["CREATED"]

    @pytest.mark.parametrize("color_data,test_description", [
        (["BLACK"], "Создание заказа с цветом BLACK"),
        (["GREY"], "Создание заказа с цветом GREY"),
        (["BLACK", "GREY"], "Создание заказа с обоими цветами"),
        ([], "Создание заказа без указания цвета (пустой массив)"),
    ])
    @allure.title("Тест: Создание заказа - проверка наличия track в теле ответа")
    def test_create_order_returns_track(
        self, basic_order_data, mock_order_session_success, color_data, test_description
    ):
        """
        Тест с параметризацией по 4 вариантам цвета.
        Проверяем, что тело ответа содержит track.
        """
        order_data = {**basic_order_data, "color": color_data}
        api = OrderAPI(session=mock_order_session_success)
        response = api.create_order(order_data)

        response_json = response.json()
        assert "track" in response_json