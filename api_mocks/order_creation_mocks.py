from unittest.mock import Mock
from typing import List, Optional, Dict, Any
import random


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
    
    @staticmethod
    def create_mock_session_for_order_creation(
        status_code: int = 201,
        track_number: Optional[int] = None
    ) -> Mock:
        """Создает моковую сессию для создания заказа"""
        if track_number is None:
            track_number = random.randint(1000, 9999)
        
        mock_session = Mock()
        mock_response = OrderMocks.create_mock_response(
            status_code=status_code,
            json_data={"track": track_number}
        )
        mock_session.post.return_value = mock_response
        
        return mock_session
    
    @staticmethod
    def create_mock_session_with_side_effect(*responses: Mock) -> Mock:
        """Создает моковую сессию с последовательными ответами"""
        mock_session = Mock()
        mock_session.post.side_effect = responses
        return mock_session
    
    @staticmethod
    def get_successful_order_response(track: int = 123456) -> Dict[str, Any]:
        """Успешный ответ при создании заказа"""
        return {"track": track}
    
    @staticmethod
    def get_error_response() -> Dict[str, Any]:
        """Ответ с ошибкой"""
        return {"message": "Ошибка при создании заказа", "code": 400}