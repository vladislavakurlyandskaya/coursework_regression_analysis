import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QMainWindow, QLabel, QFileDialog
from second_form import Linear
from third_form import Multiple


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Построение регрессионных моделей анализа данных')
        self.resize(600, 450)

        self.w = None  # Внешнего окна еще нет
        self.w2 = None  # Внешнего окна еще нет

        label1 = QLabel(self)
        label1.setText("Нажмите на кнопку, чтобы загрузить исходные данные:")
        label1.setFont(QFont('Arial', 11))
        label1.adjustSize()
        label1.move(120, 20)

        ButtonOpen = QPushButton("Загрузить", self)
        ButtonOpen.resize(100, 55)
        ButtonOpen.move(250, 50)
        ButtonOpen.clicked.connect(self.openFile)

        label2 = QLabel(self)
        label2.setText("Выберите вид регрессии:")
        label2.setFont(QFont('Arial', 11))
        label2.adjustSize()
        label2.move(200, 190)

        button1 = QPushButton("Парная регрессия", self)
        button1.resize(200, 100)
        button1.move(80, 240)
        button1.clicked.connect(self.show_new_window)

        button2 = QPushButton("Множественная регрессия", self)
        button2.resize(200, 100)
        button2.move(320, 240)
        button2.clicked.connect(self.show_new_window2)

    def openFile(self):
        fname = QFileDialog.getOpenFileName()
        global filename
        filename = fname[0]

    def show_new_window(self):
        if self.w is None:
            self.w = Linear(filename)
            self.w.show()

    def show_new_window2(self):
        if self.w2 is None:
            self.w2 = Multiple(filename)
            self.w2.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
