from unittest.mock import Mock
from typing import Dict, Any, Optional
import random
from data.test_data import CourierData


class CourierLoginMocks:
    """Класс для создания моков API логина курьера"""
    
    @staticmethod
    def create_mock_response(
        status_code: int = 200,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """
        Создает моковый объект ответа для логина
        """
        mock_response = Mock()
        mock_response.status_code = status_code
        
        if json_data is not None:
            mock_response.json.return_value = json_data
        else:
            mock_response.json.return_value = {}
        
        return mock_response
    
    @staticmethod
    def create_mock_login_session(
        login_status_code: int = 200,
        login_json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """
        Создает моковую сессию только для тестов логина
        """
        mock_session = Mock()
        
        # Мок для логина курьера
        mock_login_response = CourierLoginMocks.create_mock_response(
            status_code=login_status_code,
            json_data=login_json_data
        )
        mock_session.post.return_value = mock_login_response
        
        return mock_session
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ ФИКСТУР ===
    
    @staticmethod
    def create_success_mock_session() -> Mock:
        """Создает мок для успешного логина"""
        return CourierLoginMocks.create_mock_login_session(
            login_status_code=CourierData.API_ERROR_CODES["SUCCESS"],
            login_json_data=CourierLoginMocks.get_successful_login_response()
        )
    
    @staticmethod
    def create_missing_data_mock_session() -> Mock:
        """Создает мок для ошибки недостатка данных при логине"""
        return CourierLoginMocks.create_mock_login_session(
            login_status_code=CourierData.API_ERROR_CODES["BAD_REQUEST"],
            login_json_data=CourierLoginMocks.get_missing_login_data_response()
        )
    
    @staticmethod
    def create_not_found_mock_session() -> Mock:
        """Создает мок для ошибки 'не найдено' при логине"""
        return CourierLoginMocks.create_mock_login_session(
            login_status_code=CourierData.API_ERROR_CODES["NOT_FOUND"],
            login_json_data=CourierLoginMocks.get_account_not_found_response()
        )
    
    @staticmethod
    def get_successful_login_response(courier_id: str = None) -> Dict[str, Any]:
        """Успешный ответ при логине курьера"""
        if courier_id is None:
            # Генерируем случайный ID для курьера
            courier_id = f"courier_{random.randint(10000, 99999)}"
        return {"id": courier_id}
    
    @staticmethod
    def get_missing_login_data_response() -> Dict[str, Any]:
        """Ответ при недостатке данных для логина"""
        return {
            "message": CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_LOGIN"],
            "code": CourierData.API_ERROR_CODES["BAD_REQUEST"]
        }
    
    @staticmethod
    def get_account_not_found_response() -> Dict[str, Any]:
        """Ответ при неверных учетных данных"""
        return {
            "message": CourierData.API_RESPONSE_MESSAGES["ACCOUNT_NOT_FOUND"],
            "code": CourierData.API_ERROR_CODES["NOT_FOUND"]
        }