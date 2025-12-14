from unittest.mock import Mock
from typing import Dict, Any, Optional

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
    
    @staticmethod
    def create_mock_session_with_side_effect(
        *responses: Mock
    ) -> Mock:
        """
        Создает моковую сессию с последовательными ответами
        """
        mock_session = Mock()
        mock_session.post.side_effect = responses
        return mock_session
    
    @staticmethod
    def get_successful_login_response(courier_id: str = "test_courier_id") -> Dict[str, Any]:
        """Успешный ответ при логине курьера"""
        return {"id": courier_id}
    
    @staticmethod
    def get_missing_login_data_response() -> Dict[str, Any]:
        """Ответ при недостатке данных для логина"""
        return {"message": "Недостаточно данных для входа", "code": 400}
    
    @staticmethod
    def get_account_not_found_response() -> Dict[str, Any]:
        """Ответ при неверных учетных данных"""
        return {"message": "Учетная запись не найдена", "code": 404}
    
    @staticmethod
    def get_incorrect_credentials_response() -> Dict[str, Any]:
        """Ответ при неверных учетных данных (альтернативный)"""
        return {"message": "Учетная запись не найдена", "code": 404}
    
    @staticmethod
    def create_mock_for_successful_login() -> Mock:
        """Создает мок для успешного логина"""
        return CourierLoginMocks.create_mock_response(
            status_code=200,
            json_data=CourierLoginMocks.get_successful_login_response()
        )
    
    @staticmethod
    def create_mock_for_missing_data() -> Mock:
        """Создает мок для ошибки недостатка данных"""
        return CourierLoginMocks.create_mock_response(
            status_code=400,
            json_data=CourierLoginMocks.get_missing_login_data_response()
        )
    
    @staticmethod
    def create_mock_for_not_found() -> Mock:
        """Создает мок для ошибки 'не найдено'"""
        return CourierLoginMocks.create_mock_response(
            status_code=404,
            json_data=CourierLoginMocks.get_account_not_found_response()
        )