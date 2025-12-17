from faker import Faker
from typing import List, Optional

# Инициализируем Faker с русской локалью для реалистичных данных
fake = Faker('ru_RU')
# Устанавливаем seed для детерминированной генерации
Faker.seed(42)


class CourierData:
    """Класс для хранения тестовых данных курьера и заказов"""
    
    # Константы
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Текстовые ответы API
    API_RESPONSE_MESSAGES = {
        # Логин курьера
        "INSUFFICIENT_DATA_FOR_LOGIN": "Недостаточно данных для входа",
        "ACCOUNT_NOT_FOUND": "Учетная запись не найдена",
        
        # Создание курьера
        "INSUFFICIENT_DATA_FOR_ACCOUNT_CREATION": "Недостаточно данных для создания учетной записи",
        "LOGIN_ALREADY_EXISTS": "Этот логин уже используется",
        
        # Создание заказа
        "ORDER_CREATION_ERROR": "Ошибка при создании заказа",
    }
    
    # Коды ошибок API
    API_ERROR_CODES = {
        "BAD_REQUEST": 400,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "CREATED": 201,
        "SUCCESS": 200,
        "INTERNAL_SERVER_ERROR": 500,
    }
    
    # Статические тестовые данные для негативных тестов
    INVALID_DATA = {
        "empty_login": "",
        "empty_password": "",
        "empty_first_name": "",
        "long_string_256": "a" * 256,
        "special_chars": "!@#$%^&*()",
        "cyrillic_only": "кириллица",
        "numbers_only": "1234567890",
        "spaces_only": "   ",
        "whitespace_string": "\t\n\r",
    }
    
    # Предопределенные логины для тестов
    PREDEFINED_LOGINS = {
        "valid_login": "courier_test_01",
        "duplicate_login": "courier_duplicate_01",
        "nonexistent_login": "nonexistent_user_99",
    }
    
    # Предопределенные пароли
    PREDEFINED_PASSWORDS = {
        "valid_password": "Password123!",
        "wrong_password": "WrongPass456!",
        "short_password": "123",
    }
    
    # Предопределенные имена
    PREDEFINED_NAMES = {
        "russian_name": "Иван Иванов",
        "english_name": "John Doe",
        "name_with_spaces": "  Anna Maria  ",
    }
    
    # Цвета самокатов
    SCOOTER_COLORS = {
        "BLACK": "BLACK",
        "GREY": "GREY",
        "BOTH": ["BLACK", "GREY"],
        "NONE": [],
    }
    
    # Станции метро
    METRO_STATIONS = {
        "station_1": 1,
        "station_2": 2,
        "station_3": 3,
        "station_4": 4,
        "multiple_stations": [1, 2, 3, 4],
    }
    
    @staticmethod
    def create_courier_data(login=None, password=None, first_name=None):
        """Генерация данных курьера с использованием Faker"""
        return {
            "login": login or fake.user_name()[:20],  # Ограничиваем длину
            "password": password or fake.password(
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ),
            "firstName": first_name or fake.first_name()
        }
    
    @staticmethod
    def create_order_data(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address: Optional[str] = None,
        metro_station: Optional[int] = None,
        phone: Optional[str] = None,
        rent_time: Optional[int] = None,
        delivery_date: Optional[str] = None,
        comment: Optional[str] = None,
        color: Optional[List[str]] = None
    ) -> dict:
        """Генерация данных для заказа с использованием Faker"""
        
        # Генерация реалистичных данных, если не предоставлены
        order_data = {
            "firstName": first_name or fake.first_name(),
            "lastName": last_name or fake.last_name(),
            "address": address or fake.street_address(),
            "metroStation": metro_station or fake.random_int(min=1, max=10),
            "phone": phone or fake.phone_number(),
            "rentTime": rent_time or fake.random_int(min=1, max=10),
            "deliveryDate": delivery_date or fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            "comment": comment or fake.text(max_nb_chars=50),
        }
        
        if color is not None:
            order_data["color"] = color
            
        return order_data
    
    @staticmethod
    def get_valid_courier_data():
        """Валидные данные для создания курьера"""
        return CourierData.create_courier_data()
    
    @staticmethod
    def get_courier_data_missing_login():
        """Данные курьера без логина"""
        data = CourierData.create_courier_data()
        data["login"] = ""
        return data
    
    @staticmethod
    def get_courier_data_missing_password():
        """Данные курьера без пароля"""
        data = CourierData.create_courier_data()
        data["password"] = ""
        return data
    
    @staticmethod
    def get_courier_data_missing_all_fields():
        """Данные курьера без обязательных полей"""
        return {"login": "", "password": "", "firstName": ""}
    
    @staticmethod
    def get_courier_data_only_login():
        """Данные курьера только с логином"""
        return {"login": CourierData.PREDEFINED_LOGINS["valid_login"]}
    
    @staticmethod
    def get_courier_data_only_password():
        """Данные курьера только с паролем"""
        return {"password": CourierData.PREDEFINED_PASSWORDS["valid_password"]}
    
    @staticmethod
    def get_duplicate_courier_data():
        """Данные для создания дубликата курьера"""
        return {
            "login": CourierData.PREDEFINED_LOGINS["duplicate_login"],
            "password": CourierData.PREDEFINED_PASSWORDS["valid_password"],
            "firstName": CourierData.PREDEFINED_NAMES["russian_name"]
        }
    
    @staticmethod
    def get_login_credentials():
        """Валидные данные для логина"""
        return {
            "login": CourierData.PREDEFINED_LOGINS["valid_login"],
            "password": CourierData.PREDEFINED_PASSWORDS["valid_password"]
        }
    
    @staticmethod
    def get_wrong_login_credentials():
        """Неверные данные для логина"""
        return {
            "login": CourierData.PREDEFINED_LOGINS["nonexistent_login"],
            "password": CourierData.PREDEFINED_PASSWORDS["wrong_password"]
        }