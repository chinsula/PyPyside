"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

from PySide6 import QtWidgets

from a_threads import WeatherHandler


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.lat = 0
        self.lon = 0

        self.initUi()
        self.__initSignals()
        self.weatherHandler = WeatherHandler()

    def initUi(self):
        """
        Инициализация Ui
        :return: None
        """
        self.inputLat = QtWidgets.QLineEdit()
        self.inputLat.setPlaceholderText("Введите широту")
        self.inputLon = QtWidgets.QLineEdit()
        self.inputLon.setPlaceholderText("Введите долготу")
        l_Lat_Lon = QtWidgets.QHBoxLayout()
        l_Lat_Lon.addWidget(self.inputLat)
        l_Lat_Lon.addWidget(self.inputLon)

        self.inputDelay = QtWidgets.QLineEdit()
        self.inputDelay.setPlaceholderText("Введите время задержки")

        self.outputWheather = QtWidgets.QTextEdit()

        self.pushButtonHandle = QtWidgets.QPushButton("Старт")
        self.pushButtonHandle.setCheckable(True)

        layout = QtWidgets.QVBoxLayout()

        layout.addLayout(l_Lat_Lon)
        layout.addWidget(self.inputDelay)
        layout.addWidget(self.outputWheather)
        layout.addWidget(self.pushButtonHandle)

        self.setLayout(layout)
        self.setMinimumSize(300, 140)

    def __initSignals(self):
        self.pushButtonHandle.clicked.connect(self.on_started)


    def on_started(self, status):

        self.pushButtonHandle.setText("Стоп" if status else "Старт")


        self.weatherHandler = WeatherHandler(lat=float(60.08 if not self.inputLat.text() else self.inputLat.text()),
                                             lon=float(64.47 if not self.inputLon.text() else self.inputLon.text()))
        self.weatherHandler.setDelay(int(1 if not self.inputDelay.text() else self.inputDelay.text()))
        self.weatherHandler.start()
        self.weatherHandler.sleep(self.weatherHandler.delay1)
        self.weatherHandler.wheatherHandlerSignal.connect(self.apiUpdate)


    def apiUpdate(self, data):
        self.inputDelay.setEnabled(False)
        self.inputLon.setEnabled(False)
        self.inputLat.setEnabled(False)
        self.outputWheather.setText(f"{data}")




if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()