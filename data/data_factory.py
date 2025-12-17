from data.unique_data_generator import UniqueDataGenerator
from data.test_data import CourierData


class DataFactory:
    
    @staticmethod
    def get_unique_courier_data():
        """Для фикстуры unique_courier_data"""
        return UniqueDataGenerator.generate_unique_courier_data()
    
    @staticmethod
    def get_valid_courier_data():
        """Для фикстуры courier_data"""
        return CourierData.get_valid_courier_data()
    
    @staticmethod
    def create_order_data(**kwargs):
        """Для фикстуры basic_order_data"""
        return CourierData.create_order_data(**kwargs)