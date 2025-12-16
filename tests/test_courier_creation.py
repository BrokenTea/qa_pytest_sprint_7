import pytest
import allure
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData
from data.unique_data_generator import UniqueDataGenerator


@allure.feature("Создание курьера")
@allure.story("API: POST /api/v1/courier - все тестовые сценарии")
class TestCourierCreationFinal:
    
    # 1. Тест: курьера можно создать
    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self, unique_courier_data, delete_courier):
        """Курьера можно создать с уникальными данными"""
        courier_api = CourierAPI()
        response = courier_api.create_courier(unique_courier_data)
        
        # Проверяем статус-код
        assert response.status_code == CourierData.API_ERROR_CODES["CREATED"], \
            f"Ожидался статус 201, получен {response.status_code}. Тело ответа: {response.text}"
        
        # Проверяем тело ответа
        assert response.json() == {"ok": True}, \
            f"Ожидалось {{'ok': True}}, получено {response.json()}"
        
        # Логинимся, чтобы получить ID для удаления
        login_response = courier_api.login_courier(
            unique_courier_data["login"],
            unique_courier_data["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)
    
    # 2. Тест: нельзя создать двух одинаковых курьеров
    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self, unique_courier_data, delete_courier):
        """Нельзя создать двух одинаковых курьеров с уникальными данными"""
        courier_api = CourierAPI()
        
        # Первое создание курьера
        response1 = courier_api.create_courier(unique_courier_data)
        assert response1.status_code == CourierData.API_ERROR_CODES["CREATED"]
        assert response1.json() == {"ok": True}
        
        # Второе создание с теми же данными
        response2 = courier_api.create_courier(unique_courier_data)
        
        # Проверяем код ответа
        assert response2.status_code == CourierData.API_ERROR_CODES["CONFLICT"], \
            f"Ожидался статус 409, получен {response2.status_code}"
        
        # Логинимся, чтобы получить ID для удаления
        login_response = courier_api.login_courier(
            unique_courier_data["login"],
            unique_courier_data["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)
    
    # 3. Тест: повторяющийся логин возвращает код 409 Conflict
    @allure.title("Тест: повторяющийся логин возвращает код 409 Conflict")
    def test_duplicate_login_returns_409_conflict(self, courier_data, mock_courier_session_conflict):
        """
        Проверяем, что при попытке создания курьера с уже существующим логином
        возвращается код ответа 409 Conflict
        """
        api = CourierAPI(session=mock_courier_session_conflict)
        response = api.create_courier(courier_data)
        
        # Проверяем код ответа
        assert response.status_code == CourierData.API_ERROR_CODES["CONFLICT"]
    
    # 4. Тест: курьер создан при заполнении двух обязательных полей
    @allure.title("Тест: курьер создан при заполнении двух обязательных полей")
    def test_create_courier_with_required_fields_only(self, delete_courier):
        """Курьер создан при заполнении двух обязательных полей с уникальными данными"""
        courier_api = CourierAPI()
        
        # Генерируем уникальные данные только с обязательными полями
        courier_data = UniqueDataGenerator.generate_unique_courier_data()
        # Удаляем необязательное поле firstName
        courier_data.pop("firstName", None)
        
        response = courier_api.create_courier(courier_data)
        
        # Проверяем статус-код
        assert response.status_code == CourierData.API_ERROR_CODES["CREATED"]
        
        # Проверяем тело ответа
        assert response.json() == {"ok": True}
        
        # Логинимся, чтобы получить ID для удаления
        login_response = courier_api.login_courier(
            courier_data["login"],
            courier_data["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)
    
    # 5. Тест: курьер не создается с пустым password
    @allure.title("Тест: курьер не создается с пустым password")
    def test_cannot_create_courier_with_empty_password(self, mock_courier_session_error):
        """Курьер не создался при пустом password"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных с пустым паролем
        data_with_empty_password = CourierData.get_courier_data_missing_password()
        
        response = api.create_courier(data_with_empty_password)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 6. Тест: курьер не создается с пустым login
    @allure.title("Тест: курьер не создается с пустым login")
    def test_cannot_create_courier_with_empty_login(self, mock_courier_session_error):
        """Курьер не создался при пустом login"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных с пустым логином
        data_with_empty_login = CourierData.get_courier_data_missing_login()
        
        response = api.create_courier(data_with_empty_login)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 7. Тест: курьер не создается только с полем password
    @allure.title("Тест: курьер не создается только с полем password")
    def test_cannot_create_courier_with_only_password(self, mock_courier_session_error):
        """Курьер не создался при только поле password"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных только с паролем
        data_with_only_password = CourierData.get_courier_data_only_password()
        
        response = api.create_courier(data_with_only_password)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 8. Тест: курьер не создается только с полем login
    @allure.title("Тест: курьер не создается только с полем login")
    def test_cannot_create_courier_with_only_login(self, mock_courier_session_error):
        """Курьер не создался при только поле login"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных только с логином
        data_with_only_login = CourierData.get_courier_data_only_login()
        
        response = api.create_courier(data_with_only_login)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 9. Тест: успешный запрос возвращает код 201
    @allure.title("Тест: успешный запрос возвращает код 201")
    def test_successful_request_returns_201(self, delete_courier):
        """Проверяем успешный запрос возвращает код 201 с уникальными данными"""
        courier_api = CourierAPI()
        
        # Генерируем уникальные данные
        courier_data = UniqueDataGenerator.generate_unique_courier_data()
        
        response = courier_api.create_courier(courier_data)
        
        # Проверяем статус-код
        assert response.status_code == CourierData.API_ERROR_CODES["CREATED"]
        
        # Логинимся, чтобы получить ID для удаления
        login_response = courier_api.login_courier(
            courier_data["login"],
            courier_data["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)
    
    # 10. Тест: запрос с ошибкой возвращает код 400
    @allure.title("Тест: запрос с ошибкой возвращает код 400")
    def test_error_request_returns_400(self, mock_courier_session_error):
        """Проверяем запрос с ошибкой возвращает код 400"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных без обязательных полей
        response = api.create_courier(CourierData.get_courier_data_missing_all_fields())
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 11. Тест: успешный запрос возвращает {"ok":true}
    @allure.title("Тест: успешный запрос возвращает 'ok':true")
    def test_successful_request_returns_ok_true(self, delete_courier):
        """Успешный запрос возвращает {"ok":true} с уникальными данными"""
        courier_api = CourierAPI()
        
        # Генерируем уникальные данные
        courier_data = UniqueDataGenerator.generate_unique_courier_data()
        
        response = courier_api.create_courier(courier_data)
        
        # Проверяем статус-код
        assert response.status_code == CourierData.API_ERROR_CODES["CREATED"]
        
        # Проверяем тело ответа
        assert response.json() == {"ok": True}
        
        # Логинимся, чтобы получить ID для удаления
        login_response = courier_api.login_courier(
            courier_data["login"],
            courier_data["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)
    
    # 12. Тест: ошибка при отсутствии поля login
    @allure.title("Тест: ошибка при отсутствии поля login")
    def test_error_when_login_field_missing(self, mock_courier_session_error):
        """Ошибка при отсутствии поля login"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных без логина
        data_without_login = CourierData.get_courier_data_missing_login()
        
        response = api.create_courier(data_without_login)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 13. Тест: ошибка при отсутствии поля password
    @allure.title("Тест: ошибка при отсутствии поля password")
    def test_error_when_password_field_missing(self, mock_courier_session_error):
        """Ошибка при отсутствии поля password"""
        api = CourierAPI(session=mock_courier_session_error)
        
        # Используем метод для данных без пароля
        data_without_password = CourierData.get_courier_data_missing_password()
        
        response = api.create_courier(data_without_password)
        
        # Проверяем код ошибки
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 14. Тест: ошибка при создании курьера с уже существующим логином
    @allure.title("Тест: ошибка при создании курьера с уже существующим логином")
    def test_error_when_login_already_exists(self, delete_courier):
        """Ошибка при создании курьера с уже существующим логином"""
        courier_api = CourierAPI()
        
        # Генерируем уникальные данные для первого курьера
        courier_data1 = UniqueDataGenerator.generate_unique_courier_data()
        
        # Создаем первого курьера
        response1 = courier_api.create_courier(courier_data1)
        assert response1.status_code == CourierData.API_ERROR_CODES["CREATED"]
        
        # Создаем второго курьера с таким же логином
        courier_data2 = courier_data1.copy()  # Используем те же данные
        
        response2 = courier_api.create_courier(courier_data2)
        
        # Проверяем код ответа
        assert response2.status_code == CourierData.API_ERROR_CODES["CONFLICT"]
        
        # Логинимся, чтобы получить ID первого курьера для удаления
        login_response = courier_api.login_courier(
            courier_data1["login"],
            courier_data1["password"]
        )
        
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            delete_courier(courier_id)