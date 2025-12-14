from unittest.mock import Mock
from typing import Dict, Any, Optional


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
        mock_delete_response = CourierMocks.create_mock_response(status_code=200)
        mock_session.delete.return_value = mock_delete_response
        
        return mock_session
    
    @staticmethod
    def get_successful_create_response() -> Dict[str, Any]:
        """Успешный ответ при создании курьера"""
        return {"ok": True}
    
    @staticmethod
    def get_duplicate_error_response() -> Dict[str, Any]:
        """Ответ при попытке создать дубликат курьера"""
        return {"message": "Этот логин уже используется", "code": 409}
    
    @staticmethod
    def get_missing_field_response() -> Dict[str, Any]:
        """Ответ при отсутствии обязательных полей"""
        return {"message": "Недостаточно данных для создания учетной записи", "code": 400}