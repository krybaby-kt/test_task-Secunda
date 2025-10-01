"""
Модуль базовых моделей для работы с SQLAlchemy.

Содержит абстрактный базовый класс для всех моделей базы данных,
который предоставляет удобные методы для отображения данных модели.
"""
from database.base import Base


class SQLAlchemyModel(Base):
    """
    Абстрактный базовый класс для всех моделей SQLAlchemy.
    
    Предоставляет стандартную реализацию методов __str__ и __repr__
    для удобного отображения атрибутов модели.
    """
    __abstract__ = True
    
    def __str__(self):
        """
        Возвращает строковое представление модели.
        
        Returns:
            str: Строка с именем класса и всеми атрибутами модели
        """
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        """
        Возвращает формальное строковое представление модели для отладки.
        
        Returns:
            str: Строка с именем класса и всеми атрибутами модели
        """
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"
