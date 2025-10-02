#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# Ждем пока PostgreSQL станет доступен (здоровая проверка в docker-compose сделает это автоматически)
sleep 2

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec python main.py

