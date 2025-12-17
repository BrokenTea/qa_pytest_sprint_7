import allure
import requests
from typing import List, Optional
from data.test_data import CourierData

# Класс для работы с API заказов
class OrderAPI:
    def __init__(self, session=None):
        self.base_url = CourierData.BASE_URL
        self.session = session or requests.Session()  # Используем переданную сессию или создаем новую
    
    @allure.step("Создание заказа")
    def create_order(self, data: dict):
        """POST запрос для создания нового заказа"""
        return self.session.post(f'{self.base_url}/api/v1/orders', json=data)
    
    @allure.step("Получение заказа по треку: {track}")
    def get_order_by_track(self, track: int):
        """GET запрос для получения заказа по номеру трека"""
        return self.session.get(f'{self.base_url}/api/v1/orders/track', params={"t": track})
    
    @allure.step("Принятие заказа {order_id} курьером {courier_id}")
    def accept_order(self, courier_id: int, order_id: int):
        """PUT запрос для принятия заказа курьером"""
        return self.session.put(f'{self.base_url}/api/v1/orders/accept/{order_id}', 
                               params={"courierId": courier_id})
    
    @allure.step("Получение списка заказов")
    def get_order_list(self, courier_id: int = None, metro_stations: List[int] = None, 
                       limit: int = None, page: int = None):
        """GET запрос для получения списка заказов с фильтрацией и пагинацией"""
        params = {}
        
        # Добавляем параметры фильтрации, если они переданы
        if courier_id is not None:
            params["courierId"] = courier_id
        if metro_stations:
            params["metroStation"] = metro_stations
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        
        return self.session.get(f'{self.base_url}/api/v1/orders', params=params)