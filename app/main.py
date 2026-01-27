from fastapi import FastAPI
from typing import Dict
import uvicorn
import logging
from database.config import get_settings
from database.database import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Сервисное API",
    description="API для управления событиями",
    version="1.0.0"
)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Эндпоинт проверки работоспособности для мониторинга.
    
    Returns:
        Dict[str, str]: Сообщение о статусе
    """
    logger.info("Эндпоинт health_check успешно вызван")
    return {"status": "healthy"}


if __name__ == '__main__':
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.API_VERSION)
    print(f'Debug: {settings.DEBUG}')

    print(settings.DB_HOST)
    print(settings.DB_NAME)
    print(settings.DB_USER)

    init_db(drop_all=True, with_test_data=True)
    print('Init db has been success')

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
        log_level="debug"
    )
