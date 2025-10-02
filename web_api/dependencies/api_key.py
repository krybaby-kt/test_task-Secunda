"""
Модуль для проверки API ключа.
"""
from fastapi import Header, HTTPException
from configuration.config import settings
from typing import Annotated


def require_api_key(
    api_key: Annotated[str | None, Header(alias="x-api-key", title="API Key", description="API Key")] = None
):
    """
    Проверяет API ключ.
    """
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
