from sqlalchemy import create_engine, text
from config import DATABASE_URL

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Подключение к БД успешно!")
        return True
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return False

if __name__ == "__main__":
    test_connection()