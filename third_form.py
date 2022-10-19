import numpy as np
from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QWidget, QLineEdit, QPushButton
import pandas as pd
from PyQt5.QtGui import QFont
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics


class Multiple(QWidget):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Множественная регрессия')
        self.resize(860, 570)

        label1 = QLabel(self)
        label1.setText("Исходные данные:")
        label1.setFont(QFont('Arial', 11))
        label1.adjustSize()
        label1.move(10, 20)

        label2 = QLabel(self)
        label2.setText("Параметры регрессии:")
        label2.setFont(QFont('Arial', 11))
        label2.adjustSize()
        label2.move(550, 20)

        global filename
        filename = value
        tb = Tb(self)

        dataset = pd.read_csv(filename)

        x = dataset[['Petrol_tax', 'Average_income', 'Length_road', 'Driver_license']]
        y = dataset['Petrol_consumption']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

        regressor = LinearRegression()
        regressor.fit(x_train, y_train)

        global coeff_df
        coeff_df = pd.DataFrame(regressor.coef_, x.columns, columns=['Coefficient'])
        print(coeff_df)

        label3 = QLabel(self)
        label3.setText("Petrol_tax = - 40.017 \n\nAverage_income =  - 0.065 \n\nLength_road =  - 0.005 \n\nDriver_license = 1341.862")
        label3.setFont(QFont('Arial', 9))
        label3.adjustSize()
        label3.move(550, 65)

        label4 = QLabel(self)
        label4.setText("Уравнение линейной регрессии:")
        label4.setFont(QFont('Arial', 11))
        label4.adjustSize()
        label4.move(550, 220)

        label5 = QLabel(self)
        label5.setText("y = - 40.017 * x1 - 0.065 * x2 - 0.005 * x3 + 1341.862 * x4")
        label5.setFont(QFont('Arial', 9))
        label5.adjustSize()
        label5.move(550, 250)

        label6 = QLabel(self)
        label6.setText("Значение y от x:")
        label6.setFont(QFont('Arial', 11))
        label6.adjustSize()
        label6.move(550, 300)

        self.label7 = QLabel(self)
        self.label7.setText("x1 =")
        self.label7.setFont(QFont('Arial', 9))
        self.label7.adjustSize()
        self.label7.move(550, 330)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setGeometry(580, 330, 40, 18)

        self.label8 = QLabel(self)
        self.label8.setText("x2 =")
        self.label8.setFont(QFont('Arial', 9))
        self.label8.adjustSize()
        self.label8.move(550, 360)

        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setGeometry(580, 360, 40, 18)

        self.label9 = QLabel(self)
        self.label9.setText("x3 =")
        self.label9.setFont(QFont('Arial', 9))
        self.label9.adjustSize()
        self.label9.move(550, 390)

        self.line_edit3 = QLineEdit(self)
        self.line_edit3.setGeometry(580, 390, 40, 18)

        self.label10 = QLabel(self)
        self.label10.setText("x4 =")
        self.label10.setFont(QFont('Arial', 9))
        self.label10.adjustSize()
        self.label10.move(550, 420)

        self.line_edit4 = QLineEdit(self)
        self.line_edit4.setGeometry(580, 420, 40, 18)

        self.label11 = QLabel(self)
        self.label11.setText("y = ")
        self.label11.setFont(QFont('Arial', 9))
        self.label11.adjustSize()
        self.label11.move(750, 375)

        button2 = QPushButton("Найти y", self)
        button2.resize(78, 24)
        button2.move(635, 370)
        button2.clicked.connect(self.onClicked)

        y_pred = regressor.predict(x_test)
        df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
        print(df)

        label12 = QLabel(self)
        label12.setText("Оценка алгоритма")
        label12.setFont(QFont('Arial', 11))
        label12.adjustSize()
        label12.move(20, 420)

        label13 = QLabel(self)
        label13.setText("Mean Absolute Error = {:.3f}".format(metrics.mean_absolute_error(y_test, y_pred)) + "\nMean Squared Error = {:.3f}".format(metrics.mean_squared_error(y_test, y_pred)) + "\nRoot Mean Squared Error = {:.3f}".format(np.sqrt(metrics.mean_squared_error(y_test, y_pred))))
        label13.setFont(QFont('Arial', 9))
        label13.adjustSize()
        label13.move(20, 450)

    def onClicked(self):
        x1 = self.line_edit1.text()
        x2 = self.line_edit2.text()
        x3 = self.line_edit3.text()
        x4 = self.line_edit4.text()

        Y = b1 * float(x1) + b2 * float(x2) + b3 * float(x3) + b4 * float(x4)
        self.label11.setText("y = {:.3f}".format(Y))
        self.label11.adjustSize()


class Tb(QTableWidget):
    def __init__(self, wg):
        super().__init__(wg)
        self.setGeometry(10, 65, 490, 330)
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


global b1
global b2
global b3
global b4

b1 = -40.017
b2 = -0.065
b3 = -0.005
b4 = 1341.862

