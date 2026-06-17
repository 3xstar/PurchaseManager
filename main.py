import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from ui.main_window import MainWindow
from modules_project.models.models import Base

def main():
    app = QApplication(sys.argv)
    
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    
    try:
        window = MainWindow(db_session)
        window.show()
        
        sys.exit(app.exec())
    finally:
        db_session.close()

if __name__ == "__main__":
    main()