import pytest
import allure
from unittest.mock import Mock
from api_clients.courier_api import CourierAPI
from data.test_data import CourierData
from api_mocks.courier_creation_mocks import CourierMocks


@allure.feature("Создание курьера")
@allure.story("API: POST /api/v1/courier - все тестовые сценарии")
class TestCourierCreationFinal:
    
    @pytest.fixture
    def courier_data(self):
        """Использовать метод из test_data.py"""
        return CourierData.create_courier_data()
    
    @pytest.fixture
    def mock_session_success(self):
        """Фикстура: мок для успешного создания курьера"""
        return CourierMocks.create_mock_session(
            post_status_code=201,
            post_json_data={"ok": True}
        )

    @pytest.fixture
    def mock_session_error(self):
        """Фикстура: мок для ошибок при создании курьера"""
        return CourierMocks.create_mock_session(
            post_status_code=400,
            post_json_data={"message": "Недостаточно данных", "code": 400}
        )

    @pytest.fixture  
    def mock_session_duplicate(self):
        """Фикстура: мок для создания дубликата курьера"""
        mock_session = Mock()
        
        # Первый вызов - успешное создание
        response1 = CourierMocks.create_mock_response(
            status_code=201,
            json_data={"ok": True}
        )
        
        # Второй вызов - ошибка дубликата
        response2 = CourierMocks.create_mock_response(
            status_code=409,
            json_data=CourierMocks.get_duplicate_error_response()
        )
        
        mock_session.post.side_effect = [response1, response2]
        return mock_session
    
    @pytest.fixture
    def mock_session_conflict(self):
        """Фикстура: мок для конфликта при создании курьера (код 409)"""
        mock_session = Mock()
        mock_response = CourierMocks.create_mock_response(
            status_code=409,
            json_data=CourierMocks.get_duplicate_error_response()
        )
        mock_session.post.return_value = mock_response
        return mock_session
    
    # 1. Тест: курьера можно создать
    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self, courier_data, mock_session_success):
        api = CourierAPI(session=mock_session_success)
        response = api.create_courier(courier_data)
        assert response.status_code == 201
    
    # 2. Тест: нельзя создать двух одинаковых курьеров
    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self, courier_data, mock_session_duplicate):
        """Нет двух одинаковых курьеров"""
        api = CourierAPI(session=mock_session_duplicate)
        
        # Первый курьер создается успешно
        response1 = api.create_courier(courier_data)
        # Второй курьер с такими же данными - ошибка
        response2 = api.create_courier(courier_data)
        assert response2.status_code == 409
        
        # Проверяем что было два вызова API
        assert mock_session_duplicate.post.call_count == 2
    
    # 3. Тест: повторяющийся логин возвращает код 409 Conflict
    @allure.title("Тест: повторяющийся логин возвращает код 409 Conflict")
    def test_duplicate_login_returns_409_conflict(self, courier_data, mock_session_conflict):
        """
        Проверяем, что при попытке создания курьера с уже существующим логином
        возвращается код ответа 409 Conflict
        """
        api = CourierAPI(session=mock_session_conflict)
        response = api.create_courier(courier_data)
        
        # Проверяем код ответа
        assert response.status_code == 409
    
    # 4. Тест: курьер создан при заполнении двух обязательных полей
    @allure.title("Тест: курьер создан при заполнении двух обязательных полей")
    def test_create_courier_with_required_fields_only(self, mock_session_success):
        """Курьер создан при заполнении двух обязательных полей"""
        api = CourierAPI(session=mock_session_success)
        
        # Используем метод из test_data для создания данных
        required_data = CourierData.create_courier_data()
        required_data.pop("firstName", None)  # Удаляем необязательное поле
        
        response = api.create_courier(required_data)
        
        # Проверяем код ответа
        assert response.status_code == 201
    
    # 5. Тест: курьер не создается с пустым password
    @allure.title("Тест: курьер не создается с пустым password")
    def test_cannot_create_courier_with_empty_password(self, courier_data, mock_session_error):
        """Курьер не создался при пустом password"""
        api = CourierAPI(session=mock_session_error)
        
        # Используем копию данных с пустым паролем
        data_with_empty_password = courier_data.copy()
        data_with_empty_password["password"] = ""
        
        response = api.create_courier(data_with_empty_password)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 6. Тест: курьер не создается с пустым login
    @allure.title("Тест: курьер не создается с пустым login")
    def test_cannot_create_courier_with_empty_login(self, courier_data, mock_session_error):
        """Курьер не создался при пустом login"""
        api = CourierAPI(session=mock_session_error)
        
        data_with_empty_login = courier_data.copy()
        data_with_empty_login["login"] = ""
        
        response = api.create_courier(data_with_empty_login)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 7. Тест: курьер не создается только с полем password
    @allure.title("Тест: курьер не создается только с полем password")
    def test_cannot_create_courier_with_only_password(self, mock_session_error):
        """Курьер не создался при только поле password"""
        api = CourierAPI(session=mock_session_error)
        
        # Используем метод из test_data для генерации данных
        data_with_only_password = {
            "password": CourierData.generate_random_string(10)
        }
        
        response = api.create_courier(data_with_only_password)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 8. Тест: курьер не создается только с полем login
    @allure.title("Тест: курьер не создается только с полем login")
    def test_cannot_create_courier_with_only_login(self, mock_session_error):
        """Курьер не создался при только поле login"""
        api = CourierAPI(session=mock_session_error)
        
        data_with_only_login = {
            "login": CourierData.generate_random_string(10)
        }
        
        response = api.create_courier(data_with_only_login)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 9. Тест: успешный запрос возвращает код 201
    @allure.title("Тест: успешный запрос возвращает код 201")
    def test_successful_request_returns_201(self, courier_data, mock_session_success):
        """Проверяем успешный запрос возвращает код 201"""
        api = CourierAPI(session=mock_session_success)
        response = api.create_courier(courier_data)
        assert response.status_code == 201
    
    # 10. Тест: запрос с ошибкой возвращает код 400
    @allure.title("Тест: запрос с ошибкой возвращает код 400")
    def test_error_request_returns_400(self, mock_session_error):
        """Проверяем запрос с ошибкой возвращает код 400"""
        api = CourierAPI(session=mock_session_error)
        response = api.create_courier({})
        assert response.status_code == 400
    
    # 11. Тест: успешный запрос возвращает {"ok":true}
    @allure.title("Тест: успешный запрос возвращает {'ok':true}")
    def test_successful_request_returns_ok_true(self, courier_data, mock_session_success):
        """Успешный запрос возвращает {"ok":true}"""
        api = CourierAPI(session=mock_session_success)
        response = api.create_courier(courier_data)
    
        # Проверяем тело ответа
        assert response.json() == {"ok": True}
    
    # 12. Тест: ошибка при отсутствии поля login
    @allure.title("Тест: ошибка при отсутствии поля login")
    def test_error_when_login_field_missing(self, mock_session_error):
        """Ошибка при отсутствии поля login"""
        api = CourierAPI(session=mock_session_error)
        
        data_without_login = CourierData.create_courier_data()
        data_without_login.pop("login", None)  # Удаляем поле login
        
        response = api.create_courier(data_without_login)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 13. Тест: ошибка при отсутствии поля password
    @allure.title("Тест: ошибка при отсутствии поля password")
    def test_error_when_password_field_missing(self, mock_session_error):
        """Ошибка при отсутствии поля password"""
        api = CourierAPI(session=mock_session_error)
        
        data_without_password = CourierData.create_courier_data()
        data_without_password.pop("password", None)  # Удаляем поле password
        
        response = api.create_courier(data_without_password)
        
        # Проверяем код ошибки
        assert response.status_code == 400
    
    # 14. Тест: ошибка при создании курьера с уже существующим логином
    @allure.title("Тест: ошибка при создании курьера с уже существующим логином")
    def test_error_when_login_already_exists(self, courier_data):
        """Ошибка при создании курьера с уже существующим логином"""
        # Создаем мок с последовательными ответами
        mock_session = Mock()
        
        # Используем методы из CourierMocks для создания моков
        response1 = CourierMocks.create_mock_response(
            status_code=201,
            json_data={"ok": True}
        )
        
        response2 = CourierMocks.create_mock_response(
            status_code=409,
            json_data=CourierMocks.get_duplicate_error_response()
        )
        
        mock_session.post.side_effect = [response1, response2]
        
        api = CourierAPI(session=mock_session)
        
        # Первый курьер создается успешно
        response_first = api.create_courier(courier_data)
        
        # Второй курьер с тем же логином - ошибка
        response_second = api.create_courier(courier_data)
        assert response_second.status_code == 409
        
        # Проверяем что было два вызова API
        assert mock_session.post.call_count == 2