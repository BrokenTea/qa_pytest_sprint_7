import pytest
import allure
from unittest.mock import Mock
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData
from api_mocks.courier_login_mocks import CourierLoginMocks


@allure.feature("Логин курьера")
@allure.story("API: POST /api/v1/courier/login - все тестовые сценарии")
class TestCourierLogin:
    
    @pytest.fixture
    def random_login_data(self):
        """Фикстура со случайными тестовыми данными для логина"""
        # Используем метод из test_data
        return CourierData.create_courier_data()
    
    @pytest.fixture
    def mock_session_login_success(self):
        """Фикстура: мок для успешного логина"""
        mock_session = Mock()
        mock_response = CourierLoginMocks.create_mock_response(
            status_code=200,
            json_data={"id": f"courier_{CourierData.generate_random_string(5)}"}
        )
        mock_session.post.return_value = mock_response
        return mock_session
    
    @pytest.fixture
    def mock_session_login_missing_data(self):
        """Фикстура: мок для ошибки недостатка данных (400)"""
        return CourierLoginMocks.create_mock_login_session(
            login_status_code=400,
            login_json_data={"message": "Недостаточно данных для входа"}
        )
    
    @pytest.fixture
    def mock_session_login_not_found(self):
        """Фикстура: мок для ошибки не найденной учетной записи (404)"""
        return CourierLoginMocks.create_mock_login_session(
            login_status_code=404,
            login_json_data={"message": "Учетная запись не найдена"}
        )
    
    # 1. Тест: курьер может авторизоваться - assert код 200
    @allure.title("Тест: курьер может авторизоваться")
    def test_courier_can_login(self, random_login_data, mock_session_login_success):
        """Курьер может авторизоваться"""
        api = CourierAPI(session=mock_session_login_success)
        response = api.login_courier(
            random_login_data["login"], 
            random_login_data["password"]
        )
        
        assert response.status_code == 200
    
    # 2. Тест: Успешная авторизация возвращает id - assert возвращается id
    @allure.title("Тест: Успешная авторизация возвращает id")
    def test_successful_login_returns_id(self, random_login_data, mock_session_login_success):
        """Успешная авторизация возвращает id"""
        api = CourierAPI(session=mock_session_login_success)
        response = api.login_courier(
            random_login_data["login"], 
            random_login_data["password"]
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
    
    # 3. Тест: Авторизация со всеми обязательные поля - assert код 200
    @allure.title("Тест: Авторизация со всеми обязательные поля")
    def test_login_with_all_required_fields(self, mock_session_login_success):
        """Авторизация со всеми обязательными полями"""
        api = CourierAPI(session=mock_session_login_success)
        
        # Используем метод из test_data
        login_data = CourierData.create_courier_data()
        response = api.login_courier(login_data["login"], login_data["password"])
        
        assert response.status_code == 200
    
    # 4. Тест: Нельзя авторизироваться только с login - assert код 400
    @allure.title("Тест: Нельзя авторизироваться только с login")
    def test_cannot_login_with_only_login(self, mock_session_login_missing_data):
        """Нельзя авторизироваться только с login"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        # Используем метод из test_data для генерации логина
        login = CourierData.generate_random_string(10)
        response = api.login_courier(login, "")
        
        assert response.status_code == 400
    
    # 5. Тест: Нельзя авторизироваться только с password - assert код 400
    @allure.title("Тест: Нельзя авторизироваться только с password")
    def test_cannot_login_with_only_password(self, mock_session_login_missing_data):
        """Нельзя авторизироваться только с password"""
        api = CourierAPI(session=mock_session_login_missing_data)
        
        password = CourierData.generate_random_string(10)
        response = api.login_courier("", password)
        
        assert response.status_code == 400
    
    # 6. Тест: Нельзя авторизироваться без обязательных данных - assert код 400
    @allure.title("Тест: Нельзя авторизироваться без обязательных данных")
    def test_cannot_login_without_required_data(self, mock_session_login_missing_data):
        """Нельзя авторизироваться без обязательных данных"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("", "")
        
        assert response.status_code == 400
    
    # 7. Тест: Система вернёт ошибку, если неправильно указать login - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login")
    def test_error_when_wrong_login(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать login"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        # Используем метод из test_data для генерации данных
        login_data = CourierData.create_courier_data()
        response = api.login_courier(f"wrong_{login_data['login']}", login_data["password"])
        
        assert response.status_code == 404
    
    # 8. Тест: Система вернёт ошибку, если неправильно указать password - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать password")
    def test_error_when_wrong_password(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        login_data = CourierData.create_courier_data()
        response = api.login_courier(login_data["login"], f"wrong_{login_data['password']}")
        
        assert response.status_code == 404
    
    # 9. Тест: Система вернёт ошибку, если неправильно указать login и password - assert код 404
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login и password")
    def test_error_when_wrong_login_and_password(self, mock_session_login_not_found):
        """Система вернёт ошибку, если неправильно указать login и password"""
        api = CourierAPI(session=mock_session_login_not_found)
        
        login_data = CourierData.create_courier_data()
        response = api.login_courier(f"wrong_{login_data['login']}", f"wrong_{login_data['password']}")
        
        assert response.status_code == 404
    
    # 10. Тест: Верное тело ответа авторизироваться только с login - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться только с login")
    def test_response_body_when_only_login(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации только с login"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("test_login", "")
        
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    # 11. Тест: Верное тело ответа авторизироваться только с password - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться только с password")
    def test_response_body_when_only_password(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации только с password"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("", "test_password")
        
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    # 12. Тест: Верное тело ответа авторизироваться без обязательных данных - "message": "Недостаточно данных для входа"
    @allure.title("Тест: Верное тело ответа авторизироваться без обязательных данных")
    def test_response_body_when_no_required_data(self, mock_session_login_missing_data):
        """Верное тело ответа при авторизации без обязательных данных"""
        api = CourierAPI(session=mock_session_login_missing_data)
        response = api.login_courier("", "")
        
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    # 13. Тест: Система вернёт ошибку, если неправильно указать login - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login")
    def test_error_response_body_when_wrong_login(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать login"""
        api = CourierAPI(session=mock_session_login_not_found)
        response = api.login_courier("wrong_login", "correct_password")
        
        assert response.json()["message"] == "Учетная запись не найдена"
    
    # 14. Тест: Система вернёт ошибку, если неправильно указать password - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать password")
    def test_error_response_body_when_wrong_password(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать password"""
        api = CourierAPI(session=mock_session_login_not_found)
        response = api.login_courier("correct_login", "wrong_password")
        
        assert response.json()["message"] == "Учетная запись не найдена"
    
    # 15. Тест: Система вернёт ошибку, если неправильно указать login и password - "message": "Учетная запись не найдена"
    @allure.title("Тест: Система вернёт ошибку, если неправильно указать login и password")
    def test_error_response_body_when_wrong_credentials(self, mock_session_login_not_found):
        """Система вернёт ошибку с телом ответа, если неправильно указать login и password"""
        api = CourierAPI(session=mock_session_login_not_found)
        response = api.login_courier("wrong_login", "wrong_password")
        
        assert response.json()["message"] == "Учетная запись не найдена"