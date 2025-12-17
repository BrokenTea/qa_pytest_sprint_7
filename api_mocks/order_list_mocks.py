from unittest.mock import Mock
from typing import List, Optional, Dict, Any
import random
from data.test_data import CourierData


class OrderListMocks:
    """Класс для создания моков API списка заказов"""
    
    @staticmethod
    def create_mock_response(
        status_code: int = 200,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """Создает моковый объект ответа"""
        mock_response = Mock()
        mock_response.status_code = status_code
        
        if json_data is not None:
            mock_response.json.return_value = json_data
        else:
            mock_response.json.return_value = {}
        
        return mock_response
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ ФИКСТУР ===
    
    @staticmethod
    def create_basic_mock_session() -> Mock:
        """Создает мок для базового получения списка заказов с поддержкой пагинации"""
        mock_session = Mock()
        
        # Генерируем 35 заказов для базового теста
        all_orders = OrderListMocks.generate_orders_list(35)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = CourierData.API_ERROR_CODES["SUCCESS"]
            
            # Получаем параметры запроса
            current_limit = params.get("limit", 30) if params else 30
            current_page = params.get("page", 0) if params else 0
            
            # Применяем пагинацию
            start_idx = current_page * current_limit
            end_idx = start_idx + current_limit
            paginated_orders = all_orders[start_idx:end_idx]
            
            response.json.return_value = {"orders": paginated_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        return mock_session
    
    @staticmethod
    def create_filtered_mock_session(
        courier_id: Optional[int] = None,
        metro_stations: Optional[List[int]] = None
    ) -> Mock:
        """Создает мок для получения списка заказов с фильтрацией"""
        mock_session = Mock()
        
        # Генерируем 100 заказов
        all_orders = OrderListMocks.generate_orders_list(100)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = CourierData.API_ERROR_CODES["SUCCESS"]
            
            # Определяем запрошенные параметры
            requested_courier_id = params.get("courierId") if params else None
            requested_metro_stations = params.get("metroStation") if params else None
            requested_limit = params.get("limit", 30) if params else 30
            requested_page = params.get("page", 0) if params else 0
            
            # Фильтрация заказов
            filtered_orders = all_orders.copy()
            
            # Фильтр по курьеру
            if requested_courier_id is not None:
                requested_courier_id = int(requested_courier_id)  # Преобразуем в int
                filtered_orders = [
                    order for order in filtered_orders 
                    if order.get("courierId") == requested_courier_id
                ]
            
            # Фильтр по станциям метро
            if requested_metro_stations is not None:
                # Если metroStation передан как список
                if isinstance(requested_metro_stations, list):
                    requested_metro_stations = [int(x) for x in requested_metro_stations]  # Преобразуем в int
                    filtered_orders = [
                        order for order in filtered_orders 
                        if order.get("metroStation") in requested_metro_stations
                    ]
                else:
                    # Если metroStation передан как одно значение
                    requested_metro_stations = int(requested_metro_stations)
                    filtered_orders = [
                        order for order in filtered_orders 
                        if order.get("metroStation") == requested_metro_stations
                    ]
            
            # Пагинация
            start_idx = requested_page * requested_limit
            end_idx = start_idx + requested_limit
            paginated_orders = filtered_orders[start_idx:end_idx]
            
            response.json.return_value = {"orders": paginated_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        return mock_session
    
    @staticmethod
    def create_pagination_mock_session() -> Mock:
        """Создает мок для тестирования пагинации"""
        mock_session = Mock()
        
        # Генерируем 100 заказов
        all_orders = OrderListMocks.generate_orders_list(100)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = CourierData.API_ERROR_CODES["SUCCESS"]
            
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
        return mock_session
    
    @staticmethod
    def create_limit_test_mock_session() -> Mock:
        """Создает мок для тестов параметра limit"""
        mock_session = Mock()
        
        # Генерируем 100 заказов
        all_orders = OrderListMocks.generate_orders_list(100)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = CourierData.API_ERROR_CODES["SUCCESS"]
            
            # Получаем запрошенный limit
            requested_limit = params.get("limit") if params else None
            if requested_limit is not None:
                requested_limit = int(requested_limit)
            else:
                requested_limit = 30  # По умолчанию
            
            # Ограничиваем количество
            limited_orders = all_orders[:requested_limit]
            
            response.json.return_value = {"orders": limited_orders}
            return response
        
        mock_session.get.side_effect = mock_get
        return mock_session
    
    @staticmethod
    def create_default_values_mock_session() -> Mock:
        """Создает мок для теста дефолтных значений параметров"""
        mock_session = Mock()
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = CourierData.API_ERROR_CODES["SUCCESS"]
            
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
        return mock_session
    
    # === СУЩЕСТВУЮЩИЕ МЕТОДЫ ===
    
    @staticmethod
    def generate_order_data(
        order_id: int = None,
        courier_id: Optional[int] = None,
        metro_station: int = 4,
        track: int = None,
        status: int = 1
    ) -> Dict[str, Any]:
        """Генерация данных одного заказа"""
        if order_id is None:
            order_id = random.randint(1000, 9999)
        if track is None:
            track = random.randint(100000, 999999)
        
        order = {
            "id": order_id,
            "track": track,
            "status": status,
            "metroStation": metro_station,
            "firstName": f"Иван{order_id}",
            "lastName": f"Иванов{order_id}",
            "address": f"ул. Пушкина, д. {order_id}",
            "phone": f"+7999{order_id:07d}",
            "deliveryDate": "2024-12-31",
            "rentTime": 5
        }
        
        if courier_id is not None:
            order["courierId"] = courier_id
            
        return order
    
    @staticmethod
    def generate_orders_list(count: int = 30, courier_id: Optional[int] = None, metro_station: Optional[int] = None) -> List[Dict[str, Any]]:
        """Генерация списка заказов"""
        orders = []
        for i in range(count):
            order_kwargs = {}
            if courier_id is not None:
                order_kwargs['courier_id'] = courier_id
            if metro_station is not None:
                order_kwargs['metro_station'] = metro_station
            order_kwargs['order_id'] = 1000 + i
            orders.append(OrderListMocks.generate_order_data(**order_kwargs))
        return orders