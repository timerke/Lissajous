import json
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import PyQt5.QtWidgets as qt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5 import QtCore, QtGui
from lissajousgen import Lissajous_figure, Lissajous_generator

# Путь к директории с исходным кодом
DIR = os.path.dirname(os.path.realpath(__file__))

# Настройки фигуры по умолчанию
DEFAULT_SETTINGS = {
    'freq_x': 2,
    'freq_y': 3,
    'resolution': 100,
    'color': 'midnightblue',
    'width': 2
}

# Цвета для matplotlib
with open(os.path.join(DIR, 'mpl.json'), mode='r', encoding='utf-8') as f:
    COLOR_DICT = json.load(f)


class Lissajous_window(qt.QWidget):
    """Класс для главного окна приложения."""

    def __init__(self):

        super().__init__()

        # Ставим версию и иконку
        filename = os.path.join(DIR, 'version.txt')
        with open(filename, 'r') as f:
            version = f.readline()
        self.setWindowTitle(f'Генератор фигур Лиссажу. Версия {version}. '
                            f'CC BY-SA 4.0 Ivanov')
        filename = os.path.join(DIR, 'icon.bmp')
        self.setWindowIcon(QtGui.QIcon(filename))
        # Создаем графический интерфейс
        self.init_ui()
        # Строим фигуру с настройками по умолчанию
        self.plot_lissajous_figure()

    def _create_form_layout(self):
        """Метод создает форму с полями, регулирующими фигуру Лиссажу.
        :return: форма с полями."""

        # Создаем макет формы
        form_layout = qt.QFormLayout()
        # Поле для частоты по оси x. В поле можно вводить вещественные числа
        self.freq_x_lineedit = qt.QLineEdit()
        self.freq_x_lineedit.setText(str(DEFAULT_SETTINGS['freq_x']))
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]*[\.]?[0-9]*'))
        self.freq_x_lineedit.setValidator(validator)
        form_layout.addRow(qt.QLabel('Частота X'), self.freq_x_lineedit)
        # Поле для частоты по оси y. В поле можно вводить вещественные числа
        self.freq_y_lineedit = qt.QLineEdit()
        self.freq_y_lineedit.setText(str(DEFAULT_SETTINGS['freq_y']))
        self.freq_y_lineedit.setValidator(validator)
        form_layout.addRow(qt.QLabel('Частота Y'), self.freq_y_lineedit)
        # Поле для количества точек кривой. В поле можно вводить целые числа
        self.resolution_lineedit = qt.QLineEdit()
        self.resolution_lineedit.setText(str(DEFAULT_SETTINGS['resolution']))
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('[1-9][0-9]*'))
        self.resolution_lineedit.setValidator(validator)
        form_layout.addRow(qt.QLabel('Количество точек'),
                           self.resolution_lineedit)
        # Поле для цвета линии
        self.color_combobox = qt.QComboBox()
        self.color_combobox.addItems(COLOR_DICT.keys())
        color = ''
        for key, value in COLOR_DICT.items():
            if value == DEFAULT_SETTINGS['color']:
                color = key
                break
        self.color_combobox.setCurrentText(color)
        form_layout.addRow(qt.QLabel('Цвет линии'), self.color_combobox)
        # Поле для толщины линии
        self.width_combobox = qt.QComboBox()
        self.width_combobox.addItems(('1', '2', '3', '4'))
        self.width_combobox.setCurrentText(str(DEFAULT_SETTINGS['width']))
        form_layout.addRow(qt.QLabel('Толщина линии'), self.width_combobox)
        #
        group = qt.QGroupBox('Параметры фигуры Лиссажу')
        group.setLayout(form_layout)
        return group

    def init_ui(self):
        """Метод располагает виджеты на главном окне."""

        # Кнопки
        plot_button = qt.QPushButton('Обновить фигуру')
        plot_button.clicked.connect(self.plot_button_click_handler)
        save_button = qt.QPushButton('Сохранить фигуру')
        save_button.clicked.connect(self.save_button_click_handler)

        # Добавляем форму и кнопки в вертикальный макет, который располагается
        # справа
        vbox = qt.QVBoxLayout()
        vbox.addWidget(self._create_form_layout())
        vbox.addWidget(plot_button)
        vbox.addWidget(save_button)
        vbox.addStretch(1)

        # Создаем холст matplotlib
        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        # Добавляем на холст matplotlib область для построения графиков
        self._ax = self._fig.add_subplot(1, 1, 1)
        # Создаем qt-виджет холста для встраивания холста matplotlib fig в окно
        self._fc = FigureCanvas(self._fig)
        self._fc.setParent(self)

        hbox = qt.QHBoxLayout()
        hbox.addWidget(self._fc, 1)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def plot_lissajous_figure(self, settings=DEFAULT_SETTINGS):
        """Метод рисует фигуру Лиссажу."""

        # Удаляем устаревшие данные с графика
        self._ax.clear()
        # Генерируем сигнал для построения
        self.generator = Lissajous_generator(settings['resolution'])
        figure = self.generator.generate_figure(settings['freq_x'],
                                                settings['freq_y'])
        # Строим график
        self._ax.plot(figure.x_arr, figure.y_arr,
                      color=settings['color'], linewidth=settings['width'])
        plt.axis('off')
        # Нужно, чтобы все элементы не выходили за пределы холста
        plt.tight_layout()
        # Обновляем холст в окне
        self._fc.draw()

    def plot_button_click_handler(self):
        """Обработчик нажатия на кнопку 'Обновить фигуру'."""

        # Получаем данные из текстовых полей
        settings = {}
        settings['freq_x'] = float(self.freq_x_lineedit.text())
        settings['freq_y'] = float(self.freq_y_lineedit.text())
        settings['resolution'] = int(self.resolution_lineedit.text())
        settings['color'] = COLOR_DICT[self.color_combobox.currentText()]
        settings['width'] = int(self.width_combobox.currentText())
        # Перестраиваем график
        self.plot_lissajous_figure(settings)

    def save_button_click_handler(self):
        """Обработчик нажатия на кнопку 'Сохранить фигуру'."""

        # Определяем имя файла, куда сохранить фигуру
        filename, extension = qt.QFileDialog.getSaveFileName(
            self, 'Сохранение изображения', DIR,
            'PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*)')
        # Определяем расширение файла
        if extension == 'PNG(*.png)':
            extension = 'png'
        elif extension == 'JPEG(*.jpg *.jpeg)':
            extension = 'jpg'
        # Если не указано имя или расширение неверное, не сохраняем фигуру
        if filename == '' or extension not in ('png', 'jpg'):
            return
        self._fig.savefig(filename, format=extension)


if __name__ == "__main__":

    # Инициализируем приложение Qt
    app = qt.QApplication(sys.argv)
    # Создаём и настраиваем главное окно
    main_window = Lissajous_window()
    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
