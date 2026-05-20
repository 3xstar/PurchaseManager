# Конфигурация проекта
import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружжения
load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройка БД
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "purchase_manager")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Строка подключения
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Настройка приложения
APP_NAME = os.getenv("APP_NAME", "Менеджер покупок")
APP_VERSION = os.getenv("APP_VERSION", "0.0.1")
APP_ENV = os.getenv("APP_ENV", "development")

# Пути
QML_DIR = BASE_DIR / "app" / "ui" / "qml"
RESOURCE_DIR = BASE_DIR / "app" / "resources"