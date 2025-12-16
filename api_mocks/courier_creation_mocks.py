from unittest.mock import Mock
from typing import Dict, Any, Optional
from data.test_data import CourierData


class CourierMocks:
    """Класс для создания моков API курьера"""
    
    @staticmethod
    def create_mock_response(
        status_code: int = 201,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """
        Создает моковый объект ответа
        """
        mock_response = Mock()
        mock_response.status_code = status_code
        
        if json_data is not None:
            mock_response.json.return_value = json_data
        
        return mock_response
    
    @staticmethod
    def create_mock_session(
        post_status_code: int = 201,
        post_json_data: Optional[Dict[str, Any]] = None,
        login_status_code: int = 200,
        login_json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """
        Создает моковую сессию requests (старый метод для обратной совместимости)
        """
        return CourierMocks.create_simple_mock_session(
            post_status_code=post_status_code,
            post_json_data=post_json_data
        )
    
    @staticmethod
    def create_simple_mock_session(
        post_status_code: int = 201,
        post_json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """
        Создает простую моковую сессию для создания курьера
        """
        mock_session = Mock()
        
        # Мок для POST запросов (создание курьера)
        mock_post_response = CourierMocks.create_mock_response(
            status_code=post_status_code,
            json_data=post_json_data
        )
        mock_session.post.return_value = mock_post_response
        
        # Мок для DELETE запросов (удаление курьера)
        mock_delete_response = CourierMocks.create_mock_response(
            status_code=CourierData.API_ERROR_CODES["SUCCESS"]
        )
        mock_session.delete.return_value = mock_delete_response
        
        return mock_session
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ ФИКСТУР ===
    
    @staticmethod
    def create_success_mock_session() -> Mock:
        """Создает мок для успешного создания курьера"""
        return CourierMocks.create_mock_session(
            post_status_code=CourierData.API_ERROR_CODES["CREATED"],
            post_json_data=CourierMocks.get_successful_create_response()
        )
    
    @staticmethod
    def create_error_mock_session() -> Mock:
        """Создает мок для ошибки при создании курьера"""
        return CourierMocks.create_mock_session(
            post_status_code=CourierData.API_ERROR_CODES["BAD_REQUEST"],
            post_json_data=CourierMocks.get_missing_field_response()
        )
    
    @staticmethod
    def create_conflict_mock_session() -> Mock:
        """Создает мок для конфликта при создании курьера"""
        return CourierMocks.create_mock_session(
            post_status_code=CourierData.API_ERROR_CODES["CONFLICT"],
            post_json_data=CourierMocks.get_duplicate_error_response()
        )
    
    @staticmethod
    def create_duplicate_mock_session() -> Mock:
        """Создает мок для сценария дубликата курьера (первый успех, второй конфликт)"""
        mock_session = Mock()
        
        # Первый вызов - успешное создание
        response1 = CourierMocks.create_mock_response(
            status_code=CourierData.API_ERROR_CODES["CREATED"],
            json_data=CourierMocks.get_successful_create_response()
        )
        
        # Второй вызов - ошибка дубликата
        response2 = CourierMocks.create_mock_response(
            status_code=CourierData.API_ERROR_CODES["CONFLICT"],
            json_data=CourierMocks.get_duplicate_error_response()
        )
        
        mock_session.post.side_effect = [response1, response2]
        
        # Мок для DELETE запросов (удаление курьера)
        mock_delete_response = CourierMocks.create_mock_response(
            status_code=CourierData.API_ERROR_CODES["SUCCESS"]
        )
        mock_session.delete.return_value = mock_delete_response
        
        return mock_session
    
    @staticmethod
    def get_successful_create_response() -> Dict[str, Any]:
        """Успешный ответ при создании курьера"""
        return {"ok": True}
    
    @staticmethod
    def get_duplicate_error_response() -> Dict[str, Any]:
        """Ответ при попытке создать дубликат курьера"""
        return {
            "message": CourierData.API_RESPONSE_MESSAGES["LOGIN_ALREADY_EXISTS"],
            "code": CourierData.API_ERROR_CODES["CONFLICT"]
        }
    
    @staticmethod
    def get_missing_field_response() -> Dict[str, Any]:
        """Ответ при отсутствии обязательных полей"""
        return {
            "message": CourierData.API_RESPONSE_MESSAGES["INSUFFICIENT_DATA_FOR_ACCOUNT_CREATION"],
            "code": CourierData.API_ERROR_CODES["BAD_REQUEST"]
        }