import pytest
import allure
from api_clients.order_api import OrderAPI
from data.test_data import CourierData
from api_mocks.order_list_mocks import OrderListMocks


@allure.feature("Список заказов")
@allure.story("API: GET /api/v1/orders - получение списка заказов с фильтрацией и пагинацией")
class TestOrderList:
    
    # === 1. БАЗОВЫЕ ТЕСТЫ ПОЛУЧЕНИЯ СПИСКА ЗАКАЗОВ ===
    
    @allure.title("Тест: Получение списка заказов - возвращает статус 200")
    def test_get_orders_list_returns_200(self, mock_order_list_basic):
        """Проверяем, что запрос списка заказов возвращает статус 200"""
        api = OrderAPI(session=mock_order_list_basic)
        response = api.get_order_list()
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    @allure.title("Тест: Получение списка заказов - ответ содержит ключ 'orders'")
    def test_get_orders_list_contains_orders_key(self, mock_order_list_basic):
        """Проверяем, что ответ содержит ключ 'orders'"""
        api = OrderAPI(session=mock_order_list_basic)
        response = api.get_order_list()
        response_json = response.json()
        assert "orders" in response_json
    
    @allure.title("Тест: Получение списка заказов - значение 'orders' является списком")
    def test_get_orders_list_orders_is_list(self, mock_order_list_basic):
        """Проверяем, что значение ключа 'orders' является списком"""
        api = OrderAPI(session=mock_order_list_basic)
        response = api.get_order_list()
        response_json = response.json()
        assert isinstance(response_json["orders"], list)
    
    @allure.title("Тест: Получение списка заказов - список 'orders' не пустой")
    def test_get_orders_list_not_empty(self, mock_order_list_basic):
        """Проверяем, что список заказов не пустой"""
        api = OrderAPI(session=mock_order_list_basic)
        response = api.get_order_list()
        response_json = response.json()
        assert len(response_json["orders"]) > 0
    
    @pytest.mark.parametrize("required_field", ["id", "track", "status"])
    @allure.title("Тест: Получение списка заказов - каждый заказ содержит обязательные поля")
    def test_get_orders_list_each_order_has_required_field(self, mock_order_list_basic, required_field):
        """Проверяем, что каждый заказ содержит обязательные поля"""
        api = OrderAPI(session=mock_order_list_basic)
        response = api.get_order_list()
        response_json = response.json()
        
        for order in response_json["orders"]:
            assert required_field in order, f"Поле '{required_field}' отсутствует в заказе"
    
    # === 2. ТЕСТЫ ФИЛЬТРАЦИИ С ПАРАМЕТРИЗАЦИЕЙ ===
    
    @pytest.mark.parametrize("courier_id, metro_stations, test_description", [
        (None, None, "Без фильтров"),
        (123, None, "Только с courier_id"),
        (None, [4], "Только с одной станцией метро"),
        (None, [1, 2, 3, 4], "Только с несколькими станциями метро"),
        (123, [4], "С courier_id и одной станцией метро"),
        (123, [1, 2, 3, 4], "С courier_id и несколькими станциями метро")
    ])
    @allure.title("Тест: Фильтрация заказов - возвращает статус 200 для всех комбинаций")
    def test_get_orders_with_filters_returns_200(self, courier_id, metro_stations, test_description):
        """Проверяем, что запрос с разными фильтрами возвращает статус 200"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    @pytest.mark.parametrize("courier_id", [123, 456, 789])
    @allure.title("Тест: Фильтрация по courier_id - возвращает только заказы этого курьера")
    def test_filter_by_courier_id_returns_only_that_courier_orders(self, courier_id):
        """Проверяем, что фильтрация по courier_id возвращает только заказы указанного курьера"""
        mock_session = OrderListMocks.create_filtered_mock_session(courier_id=courier_id)
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(courier_id=courier_id)
        response_json = response.json()
        
        # Проверяем, что все заказы имеют указанный courier_id
        for order in response_json.get("orders", []):
            assert "courierId" in order
            assert order["courierId"] == courier_id
    
    @pytest.mark.parametrize("metro_stations", [
        [4],
        [1, 2],
        [1, 2, 3, 4],
        [3]
    ])
    @allure.title("Тест: Фильтрация по станциям метро - возвращает заказы только с этими станциями")
    def test_filter_by_metro_stations_returns_only_those_orders(self, metro_stations):
        """Проверяем, что фильтрация по станциям метро возвращает только заказы с этими станциями"""
        mock_session = OrderListMocks.create_filtered_mock_session(metro_stations=metro_stations)
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(metro_stations=metro_stations)
        response_json = response.json()
        
        for order in response_json.get("orders", []):
            assert order["metroStation"] in metro_stations
    
    @pytest.mark.parametrize("courier_id, metro_stations", [
        (123, [4]),
        (456, [1, 2]),
        (789, [1, 2, 3, 4]),
        (None, [3])
    ])
    @allure.title("Тест: Фильтрация - сохраняются обязательные поля заказа")
    def test_filtered_orders_preserve_required_fields(self, courier_id, metro_stations):
        """Проверяем, что при фильтрации сохраняются обязательные поля заказа"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        response_json = response.json()
        
        for order in response_json.get("orders", []):
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # === 3. ТЕСТЫ ПАРАМЕТРА LIMIT С ПАРАМЕТРИЗАЦИЕЙ ===
    
    @pytest.mark.parametrize("limit_value, expected_count", [
        (30, 30),
        (0, 0),
        (1, 1),
        (29, 29),
        (31, 31),
        (10, 10),
        (50, 50),
        (100, 100)
    ])
    @allure.title("Тест: Параметр limit - возвращает правильное количество заказов")
    def test_limit_parameter_returns_correct_number_of_orders(self, limit_value, expected_count):
        """Проверяем, что параметр limit возвращает правильное количество заказов"""
        mock_session = OrderListMocks.create_limit_test_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value)
        response_json = response.json()
        actual_count = len(response_json.get("orders", []))
        assert actual_count == expected_count, f"Ожидалось {expected_count}, получено {actual_count}"
    
    @pytest.mark.parametrize("limit_value", [5, 10, 15, 20, 25])
    @allure.title("Тест: Параметр limit - не превышает запрошенное значение")
    def test_limit_does_not_exceed_requested_value(self, limit_value):
        """Проверяем, что количество возвращаемых заказов не превышает значение limit"""
        mock_session = OrderListMocks.create_limit_test_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value)
        response_json = response.json()
        assert len(response_json.get("orders", [])) <= limit_value
    
    @allure.title("Тест: Без параметра limit возвращает 30 заказов (дефолтное значение)")
    def test_no_limit_returns_default_30_orders(self):
        """Проверяем, что без параметра limit возвращается 30 заказов (дефолтное значение)"""
        mock_session = OrderListMocks.create_limit_test_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()
        response_json = response.json()
        assert len(response_json.get("orders", [])) == 30
    
    # === 4. ТЕСТЫ ПАРАМЕТРА PAGE С ПАРАМЕТРИЗАЦИЕЙ ===
    
    @pytest.mark.parametrize("page_value, should_have_orders", [
        (0, True),
        (1, True),
        (2, True), 
        (3, True),
        (10, False)
    ])
    @allure.title("Тест: Параметр page - возвращает соответствующую страницу")
    def test_page_parameter_returns_correct_page(self, page_value, should_have_orders):
        """Проверяем, что параметр page возвращает соответствующую страницу"""
        mock_session = OrderListMocks.create_pagination_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(page=page_value, limit=10)
        response_json = response.json()
        orders = response_json.get("orders", [])
 
        assert (len(orders) > 0) == should_have_orders
    
    @pytest.mark.parametrize("page_value", [0, 1, 2, 3, 4])
    @allure.title("Тест: Разные страницы возвращают разные заказы")
    def test_different_pages_return_different_orders(self, page_value):
        """Проверяем, что разные страницы возвращают разные заказы"""
        mock_session = OrderListMocks.create_pagination_mock_session()
        api = OrderAPI(session=mock_session)
        
        # Получаем текущую страницу
        response1 = api.get_order_list(page=page_value, limit=5)
        orders1 = response1.json().get("orders", [])
        
        # Получаем следующую страницу
        response2 = api.get_order_list(page=page_value + 1, limit=5)
        orders2 = response2.json().get("orders", [])
        
        ids1 = {order["id"] for order in orders1}
        ids2 = {order["id"] for order in orders2}
            
        # Заказы на разных страницах должны быть разными
        assert ids1.isdisjoint(ids2), f"Страницы {page_value} и {page_value + 1} содержат одинаковые заказы"
    
    @allure.title("Тест: Без параметра page возвращает первую страницу (дефолтное значение)")
    def test_no_page_returns_first_page_by_default(self):
        """Проверяем, что без параметра page возвращается первая страница (дефолтное значение)"""
        mock_session = OrderListMocks.create_pagination_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=10)
        response_json = response.json()
        assert len(response_json.get("orders", [])) > 0
    
    # === 5. КОМБИНИРОВАННЫЕ ТЕСТЫ ПАГИНАЦИИ С ПАРАМЕТРИЗАЦИЕЙ ===
    
    @pytest.mark.parametrize("limit_value, page_value, expected_count", [
        (30, 0, 30),
        (10, 0, 10),
        (10, 1, 10),
        (5, 2, 5),
        (1, 4, 1),
        (20, 0, 20),
        (15, 1, 15)
    ])
    @allure.title("Тест: Комбинация limit и page - возвращает правильное количество заказов")
    def test_pagination_combination_returns_correct_count(self, limit_value, page_value, expected_count):
        """Проверяем комбинации limit и page"""
        mock_session = OrderListMocks.create_pagination_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value, page=page_value)
        response_json = response.json()
        actual_count = len(response_json.get("orders", []))
        assert actual_count == expected_count, f"Для limit={limit_value}, page={page_value}: ожидалось {expected_count}, получено {actual_count}"
    
    @pytest.mark.parametrize("limit_value, page_value", [
        (10, 0),
        (10, 1),
        (5, 2),
        (20, 0),
        (15, 1)
    ])
    @allure.title("Тест: Пагинация - количество заказов не превышает limit")
    def test_pagination_does_not_exceed_limit(self, limit_value, page_value):
        """Проверяем, что при пагинации количество заказов не превышает limit"""
        mock_session = OrderListMocks.create_pagination_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value, page=page_value)
        response_json = response.json()
        assert len(response_json.get("orders", [])) <= limit_value
    
    # === 6. КОМБИНИРОВАННЫЕ ТЕСТЫ ВСЕХ ПАРАМЕТРОВ С ПАРАМЕТРИЗАЦИЕЙ ===
    
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value", [
        (123, [4], 10, 0),
        (456, [1, 2], 20, 1),
        (None, [4], 5, 2),
        (789, None, 15, 0),
        (123, [1, 2, 3, 4], 30, 0)
    ])
    @allure.title("Тест: Все параметры вместе - возвращает статус 200")
    def test_all_parameters_together_returns_200(self, courier_id, metro_stations, limit_value, page_value):
        """Проверяем, что запрос со всеми параметрами возвращает статус 200"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    @allure.title("Тест: Все параметры вместе - фильтрация по курьеру работает (с courier_id)")
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value", [
        (123, [4], 10, 0),
        (456, [1, 2], 20, 1)
    ])
    def test_all_parameters_together_with_courier_filter(self, courier_id, metro_stations, limit_value, page_value):
        """Проверяем, что при всех параметрах фильтрация по курьеру работает, когда courier_id указан"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        response_json = response.json()
        
        # Без условия - всегда проверяем фильтрацию
        for order in response_json.get("orders", []):
            assert "courierId" in order
            assert order["courierId"] == courier_id

    @allure.title("Тест: Все параметры вместе - фильтрация по курьеру не применяется (без courier_id)")
    def test_all_parameters_together_without_courier_filter(self):
        """Проверяем, что при всех параметрах фильтрация по курьеру не применяется, когда courier_id не указан"""
        courier_id = None
        metro_stations = None
        limit_value = 15
        page_value = 0
        
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        response_json = response.json()
        
        # Когда courier_id не указан, заказы могут быть с любым courierId или без него
        # Проверяем только что ответ получен успешно
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
        assert "orders" in response_json
    
    @allure.title("Тест: Все параметры вместе - фильтрация по станциям метро работает (с metro_stations)")
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value", [
        (123, [4], 10, 0),
        (456, [1, 2], 20, 1)
    ])
    def test_all_parameters_together_with_metro_filter(self, courier_id, metro_stations, limit_value, page_value):
        """Проверяем, что при всех параметрах фильтрация по станции метро работает, когда metro_stations указаны"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        response_json = response.json()
        
        # Без условия - всегда проверяем фильтрацию
        for order in response_json.get("orders", []):
            assert order["metroStation"] in metro_stations
        
    @allure.title("Тест: Все параметры вместе - фильтрация по станциям метро не применяется (без metro_stations)")
    def test_all_parameters_together_without_metro_filter(self):
        """Проверяем, что при всех параметрах фильтрация по станции метро не применяется, когда metro_stations не указаны"""
        courier_id = None
        metro_stations = None
        limit_value = 5
        page_value = 2
        
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        
        # Проверяем только успешный ответ
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value", [
        (123, [4], 10, 0),
        (456, [1, 2], 20, 1),
        (None, [4], 5, 2),
        (789, None, 15, 0)
    ])
    @allure.title("Тест: Все параметры вместе - пагинация работает (не превышает limit)")
    def test_all_parameters_together_pagination_within_limit(self, courier_id, metro_stations, limit_value, page_value):
        """Проверяем, что при всех параметрах пагинация работает (не превышает limit)"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        response_json = response.json()
        assert len(response_json.get("orders", [])) <= limit_value
    
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value", [
        (123, [4], 10, 0),
        (456, [1, 2], 20, 1),
        (None, [4], 5, 2)
    ])
    @allure.title("Тест: Все параметры вместе - сохраняются обязательные поля")
    def test_all_parameters_together_preserves_required_fields(self, courier_id, metro_stations, limit_value, page_value):
        """Проверяем, что при всех параметрах сохраняются обязательные поля"""
        mock_session = OrderListMocks.create_filtered_mock_session(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations,
            limit=limit_value,
            page=page_value
        )
        response_json = response.json()
        
        for order in response_json.get("orders", []):
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # === 7. ТЕСТЫ ДЕФОЛТНЫХ ЗНАЧЕНИЙ ===
    
    @allure.title("Тест: Дефолтные значения - возвращает статус 200")
    def test_default_values_returns_200(self):
        """Проверяем, что запрос без параметров возвращает статус 200"""
        mock_session = OrderListMocks.create_default_values_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    @allure.title("Тест: Дефолтные значения - возвращает 30 заказов (limit=30 по умолчанию)")
    def test_default_values_returns_30_orders(self):
        """Проверяем, что запрос без параметров возвращает 30 заказов (дефолтное значение limit=30)"""
        mock_session = OrderListMocks.create_default_values_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()
        response_json = response.json()
        assert len(response_json.get("orders", [])) == 30
    
    @allure.title("Тест: Дефолтные значения - сохраняются обязательные поля")
    def test_default_values_preserves_required_fields(self):
        """Проверяем, что при дефолтных значениях сохраняются обязательные поля"""
        mock_session = OrderListMocks.create_default_values_mock_session()
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()
        response_json = response.json()
        
        for order in response_json.get("orders", []):
            assert "id" in order
            assert "track" in order
            assert "status" in order