import requests
from data.test_data import CourierData


class CourierAPI:
    def __init__(self, session=None):
        self.base_url = CourierData.BASE_URL
        self.session = session or requests.Session()
    
    def create_courier(self, data: dict):
        """Создание курьера"""
        # Используем json для передачи данных в формате JSON
        return self.session.post(f'{self.base_url}/api/v1/courier', json=data)
    
    def login_courier(self, login: str, password: str):
        """Логин курьера"""
        payload = {"login": login, "password": password}
        return self.session.post(f'{self.base_url}/api/v1/courier/login', json=payload)
    
    def delete_courier(self, courier_id: str):  # courier_id может быть строкой или числом
        """Удаление курьера"""
        return self.session.delete(f'{self.base_url}/api/v1/courier/{courier_id}')