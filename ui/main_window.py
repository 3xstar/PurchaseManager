from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QHeaderView,
    QTabWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor

from modules_project.models.models import Products
from ui.add_product_dialog import AddProductDialog
from modules_project.services.services import ProductService, ShopListService, UserService
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, db_session):
        super().__init__()
        
        self.db = db_session
        self.product_service = ProductService(self.db)
        self.shop_list_service = ShopListService(self.db)
        
        self.current_user_id = self._get_or_create_test_user()

        self.setWindowTitle("Система управления покупками")
        self.setFixedSize(1200, 750)
        
        self.setStyleSheet("""
        QMainWindow { background-color: #1e1f22; }
        QLabel { color: white; font-size: 28px; font-weight: bold; }
        QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 12px; padding: 12px; font-size: 15px; font-weight: bold; }
        QPushButton:hover { background-color: #45a049; }
        QPushButton:pressed { background-color: #3d8b40; }
        QTableWidget { background-color: #2b2d30; color: white; border: none; border-radius: 15px; font-size: 14px; gridline-color: #3c3f41; }
        QTableWidget::item { padding: 10px; }
        QHeaderView::section { background-color: #1e1f22; color: white; padding: 12px; border: none; font-size: 14px; font-weight: bold; }
        QTabWidget::pane { border: none; }
        QTabBar::tab { background: #2b2d30; color: white; padding: 12px 20px; border-radius: 10px; margin-right: 5px; }
        QTabBar::tab:selected { background: #4CAF50; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Система управления покупками")
        main_layout.addWidget(title)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.products_tab = QWidget()
        self.tabs.addTab(self.products_tab, "Продукты")

        self.expiring_tab = QWidget()
        self.tabs.addTab(self.expiring_tab, "Истекают скоро")

        products_layout = QVBoxLayout()
        self.products_tab.setLayout(products_layout)

        self.table = QTableWidget()
        self.setup_table(self.table)
        products_layout.addWidget(self.table)

        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        
        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        products_layout.addLayout(button_layout)

        expiring_layout = QVBoxLayout()
        self.expiring_tab.setLayout(expiring_layout)
        self.expiring_table = QTableWidget()
        self.setup_table(self.expiring_table)
        expiring_layout.addWidget(self.expiring_table)

        central_widget.setLayout(main_layout)
        
        self.load_products_from_db()

    def _get_or_create_test_user(self):
        """Временная функция для получения ID пользователя"""
        user_service = UserService(self.db)
        user = user_service.get_user_by_login("admin")
        if not user:
            user = user_service.create_user("admin", "admin", "Admin User")
        return user.id

    def setup_table(self, table):
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "ID", "Название", "Категория", "Количество", "Дата добавления", "Срок годности"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setSortingEnabled(True)
        
        table.setColumnHidden(0, True)

    def load_products_from_db(self):
        """Загрузка продуктов из БД в таблицу"""
        self.table.setRowCount(0)
        products = self.product_service.get_products_by_user(self.current_user_id)
        
        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)

            add_date_str = product.add_date.strftime("%d.%m.%Y") if product.add_date else ""
            expire_date_str = product.expire_date.strftime("%d.%m.%Y") if product.expire_date else ""
            category_title = product.category.title if product.category else "Без категории"
            
            items = [
                str(product.id),
                product.name,
                category_title,
                str(product.count),
                add_date_str,
                expire_date_str
            ]
            
            for col, value in enumerate(items):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
                
        self.check_expiring_products()

    def validate_product_data(self, data):
        name = data.get("name", "").strip()
        if not name:
            return "Название продукта не может быть пустым."
        if len(name) > 150:
            return "Название продукта не может превышать 150 символов."

        category = data.get("category", "").strip()
        if category and any(char.isdigit() for char in category):
            return "Категория не может содержать цифры."
        if len(category) > 100:
            return "Название категории не может превышать 100 символов."

        amount_str = data.get("amount", "").strip().replace(",", ".")
        if not amount_str:
            return "Количество не может быть пустым."
        try:
            amount = float(amount_str)
            if amount < 0:
                return "Количество не может быть отрицательным."
        except ValueError:
            return "Количество должно быть числом."

        expiry_str = data.get("expiry", "").strip()
        if expiry_str:
            try:
                expiry_date = datetime.strptime(expiry_str, "%d.%m.%Y").date()
                if expiry_date <= datetime.now().date():
                    return "Срок годности должен быть строго больше текущей даты."
            except ValueError:
                return "Неверный формат даты срока годности. Используйте ДД.ММ.ГГГГ."

        data["amount"] = str(amount)
        return None

    def add_product(self):
        dialog = AddProductDialog()
        if dialog.exec():
            data = dialog.product_data
            
            error_msg = self.validate_product_data(data)
            if error_msg:
                QMessageBox.warning(self, "Ошибка ввода", error_msg)
                return

            try:
                self.product_service.create_product(
                    user_id=self.current_user_id,
                    name=data["name"].strip(),
                    count=float(data["amount"]),
                    category_title=data["category"].strip() if data["category"].strip() else None,
                    expire_date_str=data["expiry"] if data["expiry"].strip() else None
                )
                self.load_products_from_db()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось сохранить продукт: {e}")

    def edit_product(self):
        row = self.table.currentRow()
        if row < 0:
            return

        current_id = int(self.table.item(row, 0).text())
        current_name = self.table.item(row, 1).text()
        current_category = self.table.item(row, 2).text()
        current_amount = self.table.item(row, 3).text()
        current_expiry = self.table.item(row, 5).text()

        dialog = AddProductDialog()
        
        dialog.name_input.setText(current_name)
        dialog.category_input.setText(current_category if current_category != "Без категории" else "")
        dialog.amount_input.setText(current_amount)
        
        if current_expiry:
            try:
                date_obj = QDate.fromString(current_expiry, "dd.MM.yyyy")
                dialog.expiry_input.setDate(date_obj)
            except Exception:
                pass

        if dialog.exec():
            data = dialog.product_data
            
            error_msg = self.validate_product_data(data)
            if error_msg:
                QMessageBox.warning(self, "Ошибка ввода", error_msg)
                return

            try:
                self.product_service.update_product(
                    product_id=current_id,
                    name=data["name"].strip(),
                    count=float(data["amount"]),
                    category_title=data["category"].strip() if data["category"].strip() else None,
                    expire_date_str=data["expiry"] if data["expiry"].strip() else None
                )
                self.load_products_from_db()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось обновить продукт: {e}")

    def delete_product(self):
        row = self.table.currentRow()
        if row >= 0:
            item_id = self.table.item(row, 0)
            if item_id:
                product_id = int(item_id.text())
                
                reply = QMessageBox.question(
                    self, 
                    'Подтверждение', 
                    'Вы уверены, что хотите удалить этот продукт?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        product = self.db.query(Products).filter(Products.id == product_id).first()
                        if product:
                            self.db.delete(product)
                            self.db.commit()
                            self.load_products_from_db()
                    except Exception as e:
                        self.db.rollback()
                        QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось удалить: {e}")
                        
    def check_expiring_products(self):
        self.expiring_table.setRowCount(0)
        today = datetime.now().date()
        
        for row in range(self.table.rowCount()):
            expiry_item = self.table.item(row, 5)
            if not expiry_item:
                continue
                
            try:
                expiry_date = datetime.strptime(expiry_item.text(), "%d.%m.%Y").date()
                days_left = (expiry_date - today).days
                
                if days_left <= 3 and days_left >= 0:
                    expiring_row = self.expiring_table.rowCount()
                    self.expiring_table.insertRow(expiring_row)
                    
                    for col in range(self.table.columnCount()):
                        original_item = self.table.item(row, col)
                        if original_item:
                            new_item = QTableWidgetItem(original_item.text())
                            new_item.setBackground(QColor("#ff4d4d"))
                            new_item.setForeground(QColor("white"))
                            self.expiring_table.setItem(expiring_row, col, new_item)
                            
            except ValueError:
                continue