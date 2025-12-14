import requests
from typing import List, Optional
from data.test_data import CourierData


class OrderAPI:
    def __init__(self, session=None):
        self.base_url = CourierData.BASE_URL  # Используем из test_data
        self.session = session or requests.Session()
    
    def create_order(self, data: dict):
        """Создание заказа"""
        return self.session.post(f'{self.base_url}/api/v1/orders', json=data)
    
    def get_order_by_track(self, track: int):
        """Получение заказа по трек-номеру"""
        return self.session.get(f'{self.base_url}/api/v1/orders/track', params={"t": track})
    
    def accept_order(self, courier_id: int, order_id: int):
        """Принятие заказа курьером"""
        return self.session.put(f'{self.base_url}/api/v1/orders/accept/{order_id}', 
                               params={"courierId": courier_id})
    
    def get_order_list(self, courier_id: int = None, metro_stations: List[int] = None, 
                       limit: int = None, page: int = None):
        """Получение списка заказов"""
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        if metro_stations:
            params["metroStation"] = metro_stations
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        
        return self.session.get(f'{self.base_url}/api/v1/orders', params=params)