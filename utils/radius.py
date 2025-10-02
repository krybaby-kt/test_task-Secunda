"""
Модуль для вычисления расстояния между двумя точками на Земле по формуле Haversine.
"""
from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние между двумя точками на Земле по формуле Haversine.
    
    Args:
        lat1, lon1: Широта и долгота первой точки (в градусах)
        lat2, lon2: Широта и долгота второй точки (в градусах)
    
    Returns:
        Расстояние в километрах
    """
    R = 6371.0  # Радиус Земли в километрах
    
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance