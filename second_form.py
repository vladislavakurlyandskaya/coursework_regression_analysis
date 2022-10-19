from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QLabel, QWidget, QLineEdit, QPushButton, QMessageBox
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


sns.set()
graph = 'saved_figure.png'


class Linear(QWidget):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Парная регрессия')
        self.resize(800, 550)

        label1 = QLabel(self)
        label1.setText("Исходные данные:")
        label1.setFont(QFont('Arial', 11))
        label1.adjustSize()
        label1.move(10, 20)

        label2 = QLabel(self)
        pixmap = QPixmap(graph)
        pixmap2 = pixmap.scaled(512, 384, QtCore.Qt.KeepAspectRatio)
        label2.setPixmap(pixmap2)
        label2.move(200, 160)

        global filename
        filename = value
        tb = Tb(self)

        dataset = pd.read_csv(filename)

        x = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, 1].values

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

        global regressor
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)
        dataset.plot(x='x', y='y', style='o')

        plt.title('Парная регрессия')
        plt.xlabel('x')
        plt.ylabel('y')

        predictions = regressor.predict(x)
        plt.scatter(x, y)
        plt.plot(x, predictions)
        plt.savefig(graph)

        plt.show()

        label3 = QLabel(self)
        label3.setText("Параметры регрессии:")
        label3.setFont(QFont('Arial', 11))
        label3.adjustSize()
        label3.move(200, 20)

        label4 = QLabel(self)
        label4.setText("a = {:.3f}".format(regressor.intercept_) + "\nb = {:.3f}".format(regressor.coef_[0]))
        label4.setFont(QFont('Arial', 9))
        label4.adjustSize()
        label4.move(200, 50)

        label5 = QLabel(self)
        label5.setText("Уравнение линейной регрессии:")
        label5.setFont(QFont('Arial', 11))
        label5.adjustSize()
        label5.move(200, 100)

        label6 = QLabel(self)
        label6.setText("y = {:.3f}".format(regressor.intercept_) + "+ {:.3f}".format(regressor.coef_[0]) + " * x")
        label6.setFont(QFont('Arial', 9))
        label6.adjustSize()
        label6.move(200, 130)

        label7 = QLabel(self)
        label7.setText("Значение y от x:")
        label7.setFont(QFont('Arial', 11))
        label7.adjustSize()
        label7.move(500, 20)

        self.label8 = QLabel(self)
        self.label8.setText("x =")
        self.label8.setFont(QFont('Arial', 9))
        self.label8.adjustSize()
        self.label8.move(500, 50)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setGeometry(530, 50, 40, 18)

        self.label9 = QLabel(self)
        self.label9.setText("y = ")
        self.label9.setFont(QFont('Arial', 9))
        self.label9.adjustSize()
        self.label9.move(500, 80)

        button1 = QPushButton("Найти y", self)
        button1.resize(78, 24)
        button1.move(580, 50)
        button1.clicked.connect(self.onClicked)

    def onClicked(self):
        X = self.line_edit1.text()
        Y = int(X) * float(regressor.coef_) + float(regressor.intercept_)
        self.label9.setText("y = {:.3f}".format(Y))
        self.label9.adjustSize()


class Tb(QTableWidget):
    def __init__(self, wg):
        super().__init__(wg)
        self.setGeometry(15, 50, 105, 330)
        cf = open(filename)
        data = cf.read()
        lines = data.split('\n')
        self.setColumnCount(len(lines[0].split(',')))  # количество столбцов
        self.setHorizontalHeaderLabels(lines[0].split(','))
        for i in range(1, len(lines)):  # заполнение таблицы
            if lines[i].strip() == '':
                continue
            self.setRowCount(self.rowCount() + 1)  # задать количество строк
            j, p = 0, lines[i].split(',')
            for t in p:
                self.setItem(i - 1, j, Tbi(t))  # задать поля в строке
                j += 1
        self.resizeColumnsToContents()  # ширина столцов подогнать по ширине текста


class Tbi(QTableWidgetItem):
    def __init__(self, t):
        super().__init__(t)