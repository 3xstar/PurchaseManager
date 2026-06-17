from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit
)

from PyQt6.QtCore import QDate


class AddProductDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить продукт")

        self.setFixedSize(400, 450)

        self.product_data = None

        self.setStyleSheet("""

        QDialog {
            background-color: #2b2d30;
        }

        QLabel {
            color: white;
            font-size: 14px;
            font-weight: bold;
        }

        QLineEdit {

            background-color: #3c3f41;

            color: white;

            border: 2px solid #555;

            border-radius: 8px;

            padding: 10px;

            font-size: 14px;
        }

        QDateEdit {

            background-color: #3c3f41;

            color: white;

            border: 2px solid #555;

            border-radius: 8px;

            padding: 10px;

            font-size: 14px;
        }

        QPushButton {

            background-color: #4CAF50;

            color: white;

            border: none;

            border-radius: 10px;

            padding: 12px;

            font-size: 15px;

            font-weight: bold;
        }

        QPushButton:hover {

            background-color: #45a049;
        }

        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(15)

        self.name_input = QLineEdit()

        self.category_input = QLineEdit()

        self.amount_input = QLineEdit()

        self.expiry_input = QDateEdit()

        self.expiry_input.setDate(QDate.currentDate())

        self.expiry_input.setCalendarPopup(True)

        save_button = QPushButton("Сохранить")

        save_button.clicked.connect(self.save_product)

        layout.addWidget(QLabel("Название"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Категория"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Количество"))
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("Срок годности"))
        layout.addWidget(self.expiry_input)

        layout.addStretch()

        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_product(self):

        self.product_data = {
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "amount": self.amount_input.text(),
            "expiry": self.expiry_input.date().toString("dd.MM.yyyy")
        }

        self.accept()