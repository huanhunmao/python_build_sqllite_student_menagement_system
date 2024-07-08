import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, \
    QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QToolBar, QStatusBar, QMessageBox

from PyQt6.QtGui import QAction, QIcon
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student',
                                     self)
        # 触发 添加的弹窗
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
        # 触发 Edit 的弹窗
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        # 需要加这一行 Mac 否则看不到 Help
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ('id', 'Name', 'Course', 'Mobile'))
        # 去掉第一列 id 前的 index
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolBar = QToolBar()
        toolBar.setMovable(True)
        self.addToolBar(toolBar)

        toolBar.addAction(add_student_action)
        toolBar.addAction(search_action)

        # Create status bar and status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        # 解决每次点击 重复 button 问题
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        # 确保 不重复
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        self.courses = ['Math', 'Astronomy', 'Physics', 'Biology']
        self.course_name.addItems(self.courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('mobile')
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # 插入数据
        cursor.execute(
            'INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)',
            (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        # 添加后刷新数据
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                                (name,))
        row = list(result)[0]
        items = main_window.table.findItems(row[1],
                                            Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        else:
            print("No student found with the given name.")
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Edit name
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        self.student_id = main_window.table.item(index, 0).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Edit combo box of courses
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        self.courses = ['Math', 'Astronomy', 'Physics', 'Biology', 'English']
        self.course_name.addItems(self.courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Edit mobile widget
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText('mobile')
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE students SET name=?, course=?, mobile=? WHERE id=?',
            (self.student_name.text(),
             self.course_name.currentText(),
             self.mobile.text(),
             self.student_id))

        connection.commit()
        cursor.close()
        connection.close()
        # 添加后刷新数据
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QGridLayout()

        # 是否删除弹窗
        confirmation = QLabel('Are u sure u want to delete?')
        yes = QPushButton('Yes')
        no = QPushButton('No')
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.cancel_delete)
        self.setLayout(layout)

    def delete_student(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id = ?', (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        # 关闭弹窗
        self.close()

        # 添加一条删除成功提示
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle('Success')
        confirmation_widget.setText('The record was deleted successfully!')
        confirmation_widget.exec()

    def cancel_delete(self):
        self.close()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
