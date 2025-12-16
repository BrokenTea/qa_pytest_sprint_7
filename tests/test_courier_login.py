import pytest
import allure
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData


@allure.feature("Логин курьера")
@allure.story("API: POST /api/v1/courier/login - все тестовые сценарии")
class TestCourierLogin:
    
    # 1. Тест: курьер может авторизоваться - assert код 200
    @allure.title("Тест: курьер может авторизоваться")
    def test_courier_can_login(self, random_login_data, mock_session_login_success):
        """Курьер может авторизоваться"""
        api = CourierAPI(session=mock_session_login_success)
        response = api.login_courier(
            random_login_data["login"], 
            random_login_data["password"]
        )
        
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    # 2. Тест: Успешная авторизация возвращает id - assert возвращается id
    @allure.title("Тест: Успешная авторизация возвращает id")
    def test_successful_login_returns_id(self, random_login_data, mock_session_login_success):
        """Успешная авторизация возвращает id"""
        api = CourierAPI(session=mock_session_login_success)
        response = api.login_courier(
            random_login_data["login"], 
            random_login_data["password"]
        )
        
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
        assert "id" in response.json()
    
    # 3. Тест: Авторизация со всеми обязательные поля - assert код 200
    @allure.title("Тест: Авторизация со всеми обязательные поля")
    def test_login_with_all_required_fields(self, mock_session_login_success):
        """Авторизация со всеми обязательными полями"""
        api = CourierAPI(session=mock_session_login_success)
        
        # Используем метод из test_data для получения данных логина
        login_credentials = CourierData.get_login_credentials()
        response = api.login_courier(login_credentials["login"], login_credentials["password"])
        
        assert response.status_code == CourierData.API_ERROR_CODES["SUCCESS"]
    
    # 4. Тест: Нельзя авторизироваться только с login - assert код 400
    @allure.title("Тест: Нельзя авторизироваться только с login")
    def test_cannot_login_with_only_login(self, mock_session_login_missing_data):
        """Нельзя авторизироваться только с login"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        # Используем предопределенный логин
        login = CourierData.PREDEFINED_LOGINS["valid_login"]
        response = api.login_courier(login, "")
        
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 5. Тест: Нельзя авторизироваться только с password - assert код 400
    @allure.title("Тест: Нельзя авторизироваться только с password")
    def test_cannot_login_with_only_password(self, mock_session_login_missing_data):
        """Нельзя авторизироваться только с password"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        # Используем предопределенный пароль
        password = CourierData.PREDEFINED_PASSWORDS["valid_password"]
        response = api.login_courier("", password)
        
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 6. Тест: Нельзя авторизироваться без обязательных данных - assert код 400
    @allure.title("Тест: Нельзя авторизироваться без обязательных данных")
    def test_cannot_login_without_required_data(self, mock_session_login_missing_data):
        """Нельзя авторизироваться без обязательных данных"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("", "")
        
        assert response.status_code == CourierData.API_ERROR_CODES["BAD_REQUEST"]
    
    # 7. Тест: Система вернёт ошибку, если неправильно указать login - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login")
    def test_error_when_wrong_login(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать login"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем метод из test_data для генерации данных
        wrong_credentials = CourierData.get_wrong_login_credentials()
        response = api.login_courier(wrong_credentials["login"], wrong_credentials["password"])
        
        assert response.status_code == CourierData.API_ERROR_CODES["NOT_FOUND"]
    
    # 8. Тест: Система вернёт ошибку, если неправильно указать password - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать password")
    def test_error_when_wrong_password(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем предопределенные данные
        login = CourierData.PREDEFINED_LOGINS["valid_login"]
        wrong_password = CourierData.PREDEFINED_PASSWORDS["wrong_password"]
        response = api.login_courier(login, wrong_password)
        
        assert response.status_code == CourierData.API_ERROR_CODES["NOT_FOUND"]
    
    # 9. Тест: Система вернёт ошибку, если неправильно указать login и password - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login и password")
    def test_error_when_wrong_login_and_password(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать login и password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем метод для неверных данных
        wrong_credentials = CourierData.get_wrong_login_credentials()
        response = api.login_courier(wrong_credentials["login"], wrong_credentials["password"])
        
        assert response.status_code == CourierData.API_ERROR_CODES["NOT_FOUND"]
    
    # 10. Тест: Верное тело ответа авторизироваться только с login - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться только с login")
    def test_response_body_when_only_login(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации только с login"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        # Используем предопределенный логин
        login = CourierData.PREDEFINED_LOGINS["valid_login"]
        response = api.login_courier(login, "")
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_LOGIN"]
    
    # 11. Тест: Верное тела ответа авторизироваться только с password - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться только с password")
    def test_response_body_when_only_password(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации только с password"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        # Используем предопределенный пароль
        password = CourierData.PREDEFINED_PASSWORDS["valid_password"]
        response = api.login_courier("", password)
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_LOGIN"]
    
    # 12. Тест: Верное тело ответа авторизироваться без обязательных данных - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться без обязательных данных")
    def test_response_body_when_no_required_data(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации без обязательных данных"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("", "")
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_LOGIN"]
    
    # 13. Тест: Система вернёт ошибку, если неправильно указать login - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login")
    def test_error_response_body_when_wrong_login(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать login"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем предопределенные данные
        wrong_login = CourierData.PREDEFINED_LOGINS["nonexistent_login"]
        password = CourierData.PREDEFINED_PASSWORDS["valid_password"]
        response = api.login_courier(wrong_login, password)
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["ACCOUNT_NOT_FOUND"]
    
    # 14. Тест: Система вернёт ошибку, если неправильно указать password - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать password")
    def test_error_response_body_when_wrong_password(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем предопределенные данные
        login = CourierData.PREDEFINED_LOGINS["valid_login"]
        wrong_password = CourierData.PREDEFINED_PASSWORDS["wrong_password"]
        response = api.login_courier(login, wrong_password)
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["ACCOUNT_NOT_FOUND"]
    
    # 15. Тест: Система вернёт ошибку, если неправильно указать login и password - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login и password")
    def test_error_response_body_when_wrong_credentials(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать login и password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем неверные данные
        wrong_credentials = CourierData.get_wrong_login_credentials()
        response = api.login_courier(wrong_credentials["login"], wrong_credentials["password"])
        
        assert response.json()["message"] == CourierData.API_RESPONSE_MESSAGES["ACCOUNT_NOT_FOUND"]