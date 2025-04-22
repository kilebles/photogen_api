# PhotogenAPI

## Логика

- **Auth**: залогиниться через WebApp или "test" для локалки
- **/users/updateGender**: обновить пол (`PUT /users/updateGender`)
- **/users/uploadProfile**: принимает до 10 фоток, они сохраняются в `/media/profiles`, собирается ZIP, стартуем тренинг у Replicate, возвращаем пути
- **/replicate/webhook**: ловим колбэк от Replicate, фигачим статус в БД, сохраняем `lora_id` и ссылки на результаты
- **/generations**:
  - `POST /generations` -> старт генерации по `prompt` или `category_id + style_id`, возвращаем `jobId`
  - `GET /generations/{jobId}` → чек статуса + URL картинок
- **/users/generations**: листинг всех своих сгенеренных картинок
- **/users/profiles/meta**: список своих профилей + мета (статус, фото)

## Структура

```
src/photogen_api
├── config.py       # для .env 
├── main.py         # FastAPI + StaticFiles на /media
├── auth/           # токены JWT + dep для OAuth2
├── database/       # Tortoise-модели + миграции (aerich)
├── routes/         # все API-ручки
├── services/       # логика (auth, replicate, generation и т.д.)
└── schemas/        # Pydantic-схемы
```

## Запуск

1. `poetry install`
2. Миграции: `aerich upgrade head`
3. Запуск: `uvicorn src.photogen_api.main:app --reload`

## Готово

- Сохранение фоток и ZIP
- StaticFiles на `/media`
- Запуск тренинга у Replicate (текущий/существующий LoRA)
- Webhook-обработка статусов + запись в БД
- REST-ручки для генерации картинок и чек-статуса

## В разработку

- Фоновые воркеры для многошагового pipeline (face‑swap, ratio → godmode)
- Очереди, retry, FSM‑подобные стейты (Celery/Redis или собственный планировщик)
- WebSocket/SSE для realtime уведомлений

