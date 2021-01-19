import sys, sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget



class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.btn_edit.clicked.connect(self.redaktirovat)
        self.zapros_basa()

    def zapros_basa(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(
            '''SELECT * FROM coffee''').fetchall()
        con.close()
        self.start(result)

    def start(self, result):
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса',
                 'Цена', 'Объем упаковки']
        self.table.setHorizontalHeaderLabels(title)
        if result:
            self.table.setColumnCount(len(title))
            self.table.setRowCount(0)
            for i, row in enumerate(result):
                self.table.setRowCount(
                    self.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.table.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()

    def redaktirovat(self):
        self.first_form = FirstForm(self)
        self.hide()
        self.first_form.show()


class FirstForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.btn_new.clicked.connect(self.add_zapis)
        self.btn_save.clicked.connect(self.save_table)
        self.btn_end.clicked.connect(self.end)
        self.start()

    def start(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(
            '''SELECT * FROM coffee''').fetchall()
        # if result:
        #     result = sorted(list(result), key=lambda x: x[-2], reverse=True)
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса',
                 'Цена', 'Объем упаковки']
        self.table.setHorizontalHeaderLabels(title)
        if result:
            self.table.setColumnCount(len(title))
            self.table.setRowCount(0)
            for i, row in enumerate(result):
                self.table.setRowCount(
                    self.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.table.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()
        con.close()

    def add_zapis(self):
        new_size = self.table.rowCount() + 1
        self.table.setRowCount(new_size)

        self.table.setItem(new_size - 1, 0, QTableWidgetItem(1))
        self.table.setItem(new_size - 1, 1, QTableWidgetItem("Нескафе классик"))

        for i in range(2, self.table.columnCount() - 2):
            self.table.setItem(
                new_size - 1, i, QTableWidgetItem("не известно")
            )

        self.table.setItem(
            new_size - 1, self.table.columnCount() - 2, QTableWidgetItem("0")
        )

        self.table.setItem(
            new_size - 1, self.table.columnCount() - 1, QTableWidgetItem("2")
        )
        self.table.resizeColumnsToContents()

    def save_table(self):

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute(
            f"""DELETE FROM coffee"""
        )
        for i in range(self.table.rowCount()):
            data_to_write = []
            for j in range(self.table.columnCount()):
                data_to_write.append(self.table.item(i, j).text())
            data_to_write = repr(data_to_write)[5:-1]
            cursor.execute(f"""INSERT INTO coffee VALUES ({i}, {data_to_write})""")
        connection.commit()
        connection.close()

    def end(self):
        self.main_form = Example()
        self.main_form.show()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())