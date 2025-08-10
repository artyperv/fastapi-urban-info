# Urban Info

Сервис-справочник для организаций, зданий, деятельностей

## Запуск с Docker

1. Заменить необходимое в конфигурациях:
- alembic: `backend/app/models/alembic.ini`
- config: `backend/config.yaml`

2. Запустить контейнеры:
```bash
docker compose up --build
```

## Запуск без Docker

1. Установите зависимости из под `./backend/`:

```console
$ cd backend
$ pip install -r requirements.txt
```

2. Создать базу данных
3. Заменить необходимое в конфигурациях
- alembic: `app/models/alembic.ini`
- config: `config.yaml`

4. Применить миграции
```console
$ alembic -c app/models/alembic.ini upgrade head
```

5. Запустить сервер
```console
$ python start_uvicorn.py
```

## Просмотр api
- Swagger UI: `http://127.0.0.1:8000/api/v1/docs`
- Redoc: `http://127.0.0.1:8000/api/v1/redocs`

## Примеры запросов:

- Получение всех организаций
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/' \
  -H 'accept: application/json' \
  -H 'X-API-Token: YOUR_TOKEN_HERE'
```

- Получение организаций на карте
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/by-radius/?latitude=55.751244&longitude=37.618423&radius_km=5' \
  -H 'accept: application/json' \
  -H 'X-API-Token: YOUR_TOKEN_HERE'
```
