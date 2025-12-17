from unittest.mock import Mock
from typing import List, Optional, Dict, Any
import random
from data.test_data import CourierData


class OrderMocks:
    """Класс для создания моков API заказов"""
    
    @staticmethod
    def create_mock_response(
        status_code: int = 201,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Mock:
        """Создает моковый объект ответа"""
        mock_response = Mock()
        mock_response.status_code = status_code
        
        if json_data is not None:
            mock_response.json.return_value = json_data
        else:
            mock_response.json.return_value = {}
        
        return mock_response
    
    # === НОВЫЕ МЕТОДЫ ДЛЯ ФИКСТУР ===
    
    @staticmethod
    def create_success_mock_session() -> Mock:
        """Создает мок для успешного создания заказа"""
        track_number = 123456
        
        mock_session = Mock()
        mock_response = OrderMocks.create_mock_response(
            status_code=CourierData.API_ERROR_CODES["CREATED"],
            json_data={"track": track_number}
        )
        mock_session.post.return_value = mock_response
        
        return mock_session
    
    @staticmethod
    def get_error_response() -> Dict[str, Any]:
        """Ответ с ошибкой"""
        return {
            "message": CourierData.API_RESPONSE_MESSAGES["ORDER_CREATION_ERROR"],
            "code": CourierData.API_ERROR_CODES["BAD_REQUEST"]
        }