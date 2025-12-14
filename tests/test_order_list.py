import pytest
import allure
from unittest.mock import Mock
from api_clients.order_api import OrderAPI
from data.test_data import CourierData
from api_mocks.order_list_mocks import OrderListMocks


@allure.feature("Список заказов")
@allure.story("API: GET /api/v1/orders - получение списка заказов с фильтрацией и пагинацией")
class TestOrderList:
    
    # 1. Базовый тест получения списка заказов
    @allure.title("Тест: Получение списка заказов без параметров")
    def test_get_orders_list_basic(self):
        """Проверяем, что возвращается список заказов"""
        # Создаем мок с 35 заказами
        mock_session = OrderListMocks.create_simple_mock_session(
            orders_data=OrderListMocks.generate_orders_list(35)
        )
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()
        
        # Получаем JSON ответ
        response_json = response.json()
        
        # Проверяем тело ответа содержит массив
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
        
        # Проверяем что в списке есть хотя бы один заказ
        assert len(response_json["orders"]) > 0
        
        # Проверяем обязательные поля у каждого заказа
        for order in response_json["orders"]:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 2. Тесты фильтрации с параметризацией
    @allure.title("Тест: Получение заказов с разными комбинациями фильтров")
    @pytest.mark.parametrize("courier_id, metro_stations, test_description", [
        (None, None, "Без фильтров"),
        (123, None, "Только с courier_id"),
        (None, [4], "Только с одной станцией метро"),
        (None, [1, 2, 3, 4], "Только с несколькими станциями метро"),
        (123, [4], "С courier_id и одной станцией метро"),
        (123, [1, 2, 3, 4], "С courier_id и несколькими станциями метро")
    ])
    def test_get_orders_with_different_filters(self, courier_id, metro_stations, test_description):
        """
        Проверяем различные комбинации фильтров:
        1. courier_id - возвращает активные и завершенные заказы этого курьера
        2. metro_stations - финальная выдача фильтруется по указанным станциям метро
        """
        # Создаем моковую сессию с поддержкой фильтрации
        mock_session = OrderListMocks.create_mock_session_for_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(
            courier_id=courier_id,
            metro_stations=metro_stations
        )
        
        response_json = response.json()
        orders = response_json.get("orders", [])
        
        # Проверяем фильтрацию
        if courier_id is not None:
            # У всех заказов должен быть указанный courier_id
            for order in orders:
                # Проверяем что courierId существует и равен указанному
                assert "courierId" in order, f"Заказ {order.get('id')} не имеет courierId"
                assert order.get("courierId") == courier_id, f"Ожидался courierId={courier_id}, получен {order.get('courierId')}"
        
        if metro_stations is not None:
            # У всех заказов станция метро должна быть в указанном списке
            for order in orders:
                assert order.get("metroStation") in metro_stations
        
        # Если фильтров нет, заказы могут иметь любые значения
        # Проверяем только что ответ не пустой
        assert len(orders) > 0
        
        # Проверяем обязательные поля
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 3. Тесты параметра LIMIT с параметризацией
    @allure.title("Тест: Количество заказов на странице (параметр limit)")
    @pytest.mark.parametrize("limit_value, expected_count, test_description", [
        (30, 30, "30 заказов - стандартное значение"),
        (0, 0, "0 заказов - пустой список"),
        (1, 1, "1 заказ - минимальное количество"),
        (29, 29, "29 заказов - меньше стандартного"),
        (31, 31, "31 заказ - больше стандартного"),
        (None, 30, "Параметр limit отсутствует - дефолтное значение 30"),
    ])
    def test_orders_limit_parameter(self, limit_value, expected_count, test_description):
        """
        Проверяем работу параметра limit:
        - Ограничивает количество возвращаемых заказов
        - Дефолтное значение = 30
        - 0 возвращает пустой список
        """
        # Используем специальный мок для тестов limit
        mock_session = OrderListMocks.create_mock_session_for_limit_test()
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value)
        
        response_json = response.json()
        orders = response_json.get("orders", [])
        
        # Проверяем количество возвращенных заказов
        assert len(orders) == expected_count
        
        # Проверяем что не превышает запрошенный limit
        if limit_value is not None and limit_value >= 0:
            assert len(orders) <= limit_value
        
        # Проверяем обязательные поля для всех заказов (если они есть)
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 4. Тесты параметра PAGE с параметризацией
    @allure.title("Тест: Текущая страница показа заказов (параметр page)")
    @pytest.mark.parametrize("page_value, test_description", [
        (0, "Страница 0 - первая страница"),
        (1, "Страница 1 - вторая страница"),
        (4, "Страница 4"),
        (None, "Параметр page отсутствует - дефолтное значение 0"),
    ])
    def test_orders_page_parameter(self, page_value, test_description):
        """
        Проверяем работу параметра page:
        - Определяет смещение для пагинации
        - Дефолтное значение = 0
        - Разные страницы возвращают разные данные
        """
        # Создаем мок с фиксированными данными для проверки пагинации
        mock_session = Mock()
        
        # Генерируем 100 уникальных заказов
        all_orders = []
        for i in range(100):
            all_orders.append(
                OrderListMocks.generate_order_data(
                    order_id=1000 + i,
                    track=200000 + i
                )
            )
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            
            # Получаем параметры пагинации
            current_limit = params.get("limit", 30) if params else 30
            current_page = params.get("page", 0) if params else 0
            
            # Вычисляем индексы для среза
            start_idx = current_page * current_limit
            end_idx = start_idx + current_limit
            
            # Получаем заказы для текущей страницы
            paginated_orders = all_orders[start_idx:end_idx]
            
            response.json.return_value = {"orders": paginated_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(page=page_value, limit=10)  # Используем limit=10 для теста
        
        response_json = response.json()
        orders = response_json.get("orders", [])
        
        # Проверяем что страница возвращает данные
        if page_value is None or page_value == 0:
            # Первая страница должна возвращать заказы
            assert len(orders) > 0
        
        # Для проверки разных страниц получаем первую и вторую страницу
        if page_value == 0:
            # Получаем вторую страницу
            api2 = OrderAPI(session=mock_session)
            response2 = api2.get_order_list(page=1, limit=10)
            orders2 = response2.json().get("orders", [])
            
            # Если есть заказы на второй странице, проверяем что они разные
            if orders and orders2:
                ids1 = {order["id"] for order in orders}
                ids2 = {order["id"] for order in orders2}
                
                # Заказы на разных страницах должны быть разные
                assert ids1.isdisjoint(ids2), "Заказы на разных страницах должны быть разными"
        
        # Проверяем обязательные поля
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 5. Комбинированные тесты пагинации
    @allure.title("Тест: Комбинации limit и page")
    @pytest.mark.parametrize("limit_value, page_value, test_description", [
        (30, 0, "Первая страница, 30 заказов"),
        (30, 1, "Вторая страница, 30 заказов"),
        (10, 2, "Третья страница, 10 заказов"),
        (5, 0, "Первая страница, 5 заказов"),
        (1, 4, "Пятая страница, 1 заказ")
    ])
    def test_orders_pagination_combined(self, limit_value, page_value, test_description):
        """
        Проверяем комбинации limit и page:
        - Пагинация работает корректно с разными значениями
        - Разные страницы возвращают разные данные при одинаковом limit
        """
        mock_session = Mock()
        
        # Генерируем 100 заказов
        all_orders = OrderListMocks.generate_orders_list(100)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            
            current_limit = params.get("limit", 30) if params else 30
            current_page = params.get("page", 0) if params else 0
            
            start_idx = current_page * current_limit
            end_idx = start_idx + current_limit
            
            paginated_orders = all_orders[start_idx:end_idx]
            
            response.json.return_value = {"orders": paginated_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list(limit=limit_value, page=page_value)
        
        response_json = response.json()
        orders = response_json.get("orders", [])
        
        # Вычисляем ожидаемое количество заказов
        total_orders = 100
        calculated_start_idx = page_value * limit_value
        if calculated_start_idx < total_orders:
            expected_count = min(limit_value, total_orders - calculated_start_idx)
        else:
            expected_count = 0
        
        assert len(orders) == expected_count
        
        # Проверяем что количество заказов не превышает limit
        assert len(orders) <= limit_value
        
        # Проверяем обязательные поля для всех заказов (если они есть)
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 6. Комбинированные тесты всех параметров
    @allure.title("Тест: Все параметры вместе (комбинационный тест)")
    @pytest.mark.parametrize("courier_id, metro_stations, limit_value, page_value, test_description", [
        (123, [4], 10, 0, "Фильтр по курьеру, станции, 10 на странице, первая страница"),
        (456, [1, 2, 3], 20, 1, "Фильтр по курьеру, нескольким станциям, 20 на странице, вторая страница"),
        (None, [4], 5, 2, "Фильтр по станции, 5 на странице, третья страница"),
        (789, None, 15, 0, "Фильтр по курьеру, 15 на странице, первая страница")
    ])
    def test_orders_all_parameters_combined(self, courier_id, metro_stations, limit_value, page_value, test_description):
        """
        Проверяем работу всех параметров вместе:
        - Фильтрация по courier_id работает
        - Фильтрация по metro_stations работает  
        - Пагинация (limit и page) работает
        - Все параметры совместимы друг с другом
        """
        # Создаем сложный мок с поддержкой всех параметров
        mock_session = OrderListMocks.create_mock_session_for_order_list(
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
        orders = response_json.get("orders", [])
        
        # Проверяем фильтрацию
        if courier_id is not None:
            for order in orders:
                assert "courierId" in order
                assert order.get("courierId") == courier_id
        
        if metro_stations is not None:
            for order in orders:
                assert order.get("metroStation") in metro_stations
        
        # Проверяем пагинацию
        assert len(orders) <= limit_value
        
        # Проверяем обязательные поля
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order
    
    # 7. Тест: Проверка дефолтных значений
    @allure.title("Тест: Проверка дефолтных значений параметров")
    def test_orders_default_values(self):
        """Проверяем дефолтные значения параметров"""
        mock_session = Mock()
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            
            # Проверяем дефолтные значения
            current_limit = params.get("limit", 30) if params else 30
            current_page = params.get("page", 0) if params else 0
            
            # Генерируем заказы
            all_orders = OrderListMocks.generate_orders_list(35)
            
            # Применяем пагинацию с дефолтными значениями
            start_idx = current_page * current_limit
            end_idx = start_idx + current_limit
            paginated_orders = all_orders[start_idx:end_idx]
            
            response.json.return_value = {"orders": paginated_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        
        api = OrderAPI(session=mock_session)
        response = api.get_order_list()  # Без параметров
        
        response_json = response.json()
        orders = response_json.get("orders", [])
        
        # При дефолтных значениях должно быть 30 заказов (limit=30, page=0)
        # Но у нас всего 35 заказов, так что вернется 30
        assert len(orders) == 30
        
        # Проверяем обязательные поля
        for order in orders:
            assert "id" in order
            assert "track" in order
            assert "status" in order