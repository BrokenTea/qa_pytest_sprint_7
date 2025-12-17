import allure
import requests
from data.test_data import CourierData

# Класс для работы с API курьеров
class CourierAPI:
    def __init__(self, session=None):
        self.base_url = CourierData.BASE_URL
        self.session = session or requests.Session()
    
    @allure.step("Создание курьера")
    def create_courier(self, data: dict):
        """POST запрос для создания нового курьера"""
        return self.session.post(f'{self.base_url}/api/v1/courier', json=data)
    
    @allure.step("Логин курьера")
    def login_courier(self, login: str, password: str):
        """POST запрос для аутентификации курьера"""
        payload = {"login": login, "password": password}
        return self.session.post(f'{self.base_url}/api/v1/courier/login', json=payload)
    
    @allure.step("Удаление курьера с ID: {courier_id}")
    def delete_courier(self, courier_id: str):
        """DELETE запрос для удаления курьера по ID"""
        return self.session.delete(f'{self.base_url}/api/v1/courier/{courier_id}')