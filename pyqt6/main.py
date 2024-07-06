import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        # Create widgets
        name_label = QLabel('Name:')
        self.name_line_edit = QLineEdit()

        date_label = QLabel('Date of Birth MM/DD/YYYY:')
        self.date_line_edit = QLineEdit()

        # Add button
        calculate_button = QPushButton('Calculate')
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel('')

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        # 设置的这些东西 添加到 QGridLayout 上才能展示
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.date_line_edit.text()
        try:
            # 使用 strptime 方法解析日期
            birth_date = datetime.strptime(date_of_birth, '%m/%d/%Y')
            age = current_year - birth_date.year
            # 检查是否已经过了生日
            if (datetime.now().month, datetime.now().day) < (birth_date.month, birth_date.day):
                age -= 1
            self.output_label.setText(f'{self.name_line_edit.text()} is {age} years old.')
        except ValueError:
            self.output_label.setText('Invalid date format. Please use MM/DD/YYYY.')

app = QApplication(sys.argv)
app_calculator = AgeCalculator()
app_calculator.show()
sys.exit(app.exec())
