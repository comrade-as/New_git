import sys, sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem



class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.start()

    def start(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(
            '''SELECT * FROM coffee''').fetchall()
        if result:
            result = sorted(list(result), key=lambda x: x[-2], reverse=True)
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())