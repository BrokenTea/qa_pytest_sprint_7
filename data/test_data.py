import random
import string
import requests
from typing import List, Optional

class CourierData:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    @staticmethod
    def generate_random_string(length: int) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def create_courier_data(login=None, password=None, first_name=None):
        """Генерация данных курьера"""
        return {
            "login": login or CourierData.generate_random_string(10),
            "password": password or CourierData.generate_random_string(10),
            "firstName": first_name or CourierData.generate_random_string(10)
        }
    
    @staticmethod
    def register_new_courier_and_return_login_password():
        """Метод регистрации нового курьера возвращает список из логина, пароля и имени"""
        login = CourierData.generate_random_string(10)
        password = CourierData.generate_random_string(10)
        first_name = CourierData.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{CourierData.BASE_URL}/api/v1/courier', data=payload)
        
        if response.status_code == 201:
            return [login, password, first_name]
        return []  # Возвращаем пустой список в случае ошибки
    
    @staticmethod
    def create_order_data(
        first_name: str = "Иван",
        last_name: str = "Иванов",
        address: str = "ул. Пушкина, д. 10",
        metro_station: int = 4,
        phone: str = "+79991112233",
        rent_time: int = 5,
        delivery_date: str = "2024-12-31",
        comment: str = "Тестовый заказ",
        color: Optional[List[str]] = None
    ) -> dict:
        """Генерация данных для заказа"""
        order_data = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
        }
        
        if color is not None:
            order_data["color"] = color
            
        return order_data