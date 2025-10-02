"""
Модуль для базовых настроек.
"""
import asyncio


current_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()