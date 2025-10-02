"""
Модуль репозитория телефонного номера.
"""
from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.phone_numbers import PhoneNumberModel


class PhoneNumberTool(AsyncBaseIdSQLAlchemyCRUD):
    model = PhoneNumberModel
    field_id = "id"
    lock: Lock = Lock()
