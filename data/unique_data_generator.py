import string
import time
import random


class UniqueDataGenerator:
    """Класс для генерации уникальных тестовых данных"""
    
    @staticmethod
    def generate_random_string(length=10):
        """Генерирует случайную строку заданной длины"""
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    
    @staticmethod
    def generate_unique_courier_data():
        """Генерирует уникальные данные для создания курьера"""
        login = f"courier_{int(time.time() * 1000)}_{UniqueDataGenerator.generate_random_string(5)}"
        password = UniqueDataGenerator.generate_random_string(10)
        first_name = UniqueDataGenerator.generate_random_string(10)
        
        return {
            "login": login,
            "password": password,
            "firstName": first_name
        }