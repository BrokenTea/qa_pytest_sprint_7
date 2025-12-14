from unittest.mock import Mock
from typing import List, Optional, Dict, Any
import random


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
    
    @staticmethod
    def create_mock_session_for_order_list(
        orders_count: int = 30,
        courier_id: Optional[int] = None,
        metro_stations: Optional[List[int]] = None,
        limit: int = 30,
        page: int = 0
    ) -> Mock:
        """Создает моковую сессию для получения списка заказов"""
        mock_session = Mock()
        
        # Генерация базового списка заказов
        all_orders = []
        
        for i in range(100):  # Всего 100 заказов в системе
            # Определяем courierId для заказа
            current_courier_id = None
            if courier_id is not None:
                # Для тестов с фильтром по курьеру - все заказы имеют этого курьера
                current_courier_id = courier_id
            else:
                # Для тестов без фильтра - случайные курьеры или без курьера
                if random.random() > 0.5:
                    current_courier_id = random.randint(100, 200)
            
            # Определяем станцию метро для заказа
            current_metro_station = 4  # По умолчанию
            if metro_stations is not None and metro_stations:
                current_metro_station = random.choice(metro_stations)
            else:
                current_metro_station = random.choice([1, 2, 3, 4])
            
            all_orders.append(
                OrderListMocks.generate_order_data(
                    order_id=1000 + i,
                    courier_id=current_courier_id,
                    metro_station=current_metro_station
                )
            )
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = 200
            
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
    def create_simple_mock_session(
        status_code: int = 200,
        orders_data: Optional[List[Dict[str, Any]]] = None
    ) -> Mock:
        """Создает простую моковую сессию"""
        mock_session = Mock()
        
        if orders_data is None:
            orders_data = OrderListMocks.generate_orders_list(35)
        
        mock_response = OrderListMocks.create_mock_response(
            status_code=status_code,
            json_data={"orders": orders_data}
        )
        mock_session.get.return_value = mock_response
        return mock_session
    
    @staticmethod
    def create_mock_session_for_limit_test():
        """Создает мок для тестов limit"""
        mock_session = Mock()
        
        # Генерируем 100 заказов
        all_orders = OrderListMocks.generate_orders_list(100)
        
        def mock_get(url, params=None, **kwargs):
            response = Mock()
            response.status_code = 200
            
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