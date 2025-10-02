# Docker Setup Guide

## Быстрый старт

### 1. Предварительные требования

- Установите [Docker Desktop](https://www.docker.com/products/docker-desktop) для Windows
- Запустите Docker Desktop

### 2. Запустите проект

```bash
docker-compose up --build
```

Эта команда:
- Запустит PostgreSQL в отдельном контейнере
- Дождется готовности базы данных
- Применит миграции Alembic
- Запустит FastAPI приложение

Приложение будет доступно на `http://localhost:3002`

### 3. Проверьте работу API

Откройте в браузере документацию Swagger: `http://localhost:3002/docs`

### 4. Остановить проект

```bash
docker-compose down
```

### 5. Остановить проект и удалить данные БД

```bash
docker-compose down -v
```

## Архитектура

Проект использует **микросервисную архитектуру** с отдельными контейнерами:

- **db (PostgreSQL)**: База данных на порту 5432
- **app (FastAPI)**: API сервер на порту 3002
- Контейнеры общаются через внутреннюю Docker сеть
- Данные PostgreSQL сохраняются в Docker volume `postgres_data`

## Конфигурация

Проект использует файл `.env.docker` для настроек Docker окружения:

```env
DATABASE_HOST=db          # Имя сервиса БД из docker-compose.yml
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=admin
DATABASE_NAME=test_task_secunda

BACKEND_HOST=0.0.0.0      # Слушать на всех интерфейсах
BACKEND_PORT=3002

API_KEY=your-api-key
```

**Важно**: 
- `DATABASE_HOST=db` - это имя сервиса из docker-compose.yml
- `BACKEND_HOST=0.0.0.0` - чтобы API был доступен снаружи контейнера

## Полезные команды

### Просмотр логов всех сервисов
```bash
docker-compose logs -f
```

### Просмотр логов конкретного сервиса
```bash
docker-compose logs -f app
docker-compose logs -f db
```

### Выполнение команд внутри контейнера
```bash
docker-compose exec app bash
docker-compose exec db psql -U postgres -d test_task_secunda
```

### Создание новой миграции
```bash
docker-compose exec app alembic revision --autogenerate -m "migration name"
```

### Перезапуск только приложения
```bash
docker-compose restart app
```

### Запуск в фоновом режиме
```bash
docker-compose up -d
```

### Пересборка образа
```bash
docker-compose build --no-cache
docker-compose up
```

## Troubleshooting

### Ошибка подключения к БД
Убедитесь, что в `.env.docker` параметр `DATABASE_HOST=db` (не localhost)

### База данных не готова
Docker Compose автоматически ждет готовности БД через healthcheck. Если проблемы - увеличьте sleep в entrypoint.sh

### Порты заняты
Если порт 3002 или 5432 занят, измените в docker-compose.yml:
```yaml
ports:
  - "3003:3002"  # внешний:внутренний
```

