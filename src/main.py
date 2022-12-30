import json
import os
import sys
from typing import Dict, Union
import matplotlib.pyplot as plt
import PyQt5.QtWidgets as qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui
from lissajousgen import LissajousGenerator
from version import VERSION


# Путь к директории с исходным кодом
DIR = os.path.dirname(os.path.realpath(__file__))

# Настройки фигуры по умолчанию
DEFAULT_SETTINGS = {"freq_x": 2,
                    "freq_y": 3,
                    "resolution": 100,
                    "phase_shift": 0,
                    "color": "midnightblue",
                    "width": 2}

# Цвета для matplotlib
with open(os.path.join(DIR, "mpl.json"), mode="r", encoding="utf-8") as file:
    COLOR_DICT = json.load(file)


class LissajousWindow(qt.QWidget):
    """
    Класс для главного окна приложения.
    """

    def __init__(self) -> None:
        super().__init__()
        self._generator: LissajousGenerator = LissajousGenerator()
        self._init_ui()
        self.plot_lissajous_figure()

    def _create_form_layout(self) -> qt.QGroupBox:
        """
        Метод создает форму с полями, регулирующими фигуру Лиссажу.
        :return: форма с полями.
        """

        form_layout = qt.QFormLayout()
        self.line_edit_freq_x: qt.QLineEdit = qt.QLineEdit()
        self.line_edit_freq_x.setText(str(DEFAULT_SETTINGS["freq_x"]))
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r"[0-9]*[\.]?[0-9]*"))
        self.line_edit_freq_x.setValidator(validator)
        form_layout.addRow(qt.QLabel("Частота X"), self.line_edit_freq_x)

        self.line_edit_freq_y: qt.QLineEdit = qt.QLineEdit()
        self.line_edit_freq_y.setText(str(DEFAULT_SETTINGS["freq_y"]))
        self.line_edit_freq_y.setValidator(validator)
        form_layout.addRow(qt.QLabel("Частота Y"), self.line_edit_freq_y)

        self.line_edit_phase_shift: qt.QLineEdit = qt.QLineEdit()
        self.line_edit_phase_shift.setText(str(DEFAULT_SETTINGS["phase_shift"]))
        self.line_edit_phase_shift.setValidator(validator)
        form_layout.addRow(qt.QLabel("Сдвиг фаз"), self.line_edit_phase_shift)

        self.line_edit_resolution: qt.QLineEdit = qt.QLineEdit()
        self.line_edit_resolution.setText(str(DEFAULT_SETTINGS["resolution"]))
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[1-9][0-9]*"))
        self.line_edit_resolution.setValidator(validator)
        form_layout.addRow(qt.QLabel("Количество точек"), self.line_edit_resolution)

        self.color_combobox = qt.QComboBox()
        self.color_combobox.addItems(COLOR_DICT.keys())
        color = ""
        for key, value in COLOR_DICT.items():
            if value == DEFAULT_SETTINGS["color"]:
                color = key
                break
        self.color_combobox.setCurrentText(color)
        form_layout.addRow(qt.QLabel("Цвет линии"), self.color_combobox)

        self.combobox_width = qt.QComboBox()
        self.combobox_width.addItems(list(map(str, range(1, 5))))
        self.combobox_width.setCurrentText(str(DEFAULT_SETTINGS["width"]))
        form_layout.addRow(qt.QLabel("Толщина линии"), self.combobox_width)

        group = qt.QGroupBox("Параметры фигуры Лиссажу")
        group.setLayout(form_layout)
        return group

    def _init_ui(self) -> None:
        """
        Метод располагает виджеты на главном окне.
        """

        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {VERSION}")
        self.setWindowIcon(QtGui.QIcon(os.path.join(DIR, "icon.bmp")))

        self.button_plot: qt.QPushButton = qt.QPushButton("Обновить фигуру")
        self.button_plot.clicked.connect(self.handle_click_on_button_plot)
        self.button_save: qt.QPushButton = qt.QPushButton("Сохранить фигуру")
        self.button_save.clicked.connect(self.handle_click_on_button_save)

        v_box = qt.QVBoxLayout()
        v_box.addWidget(self._create_form_layout())
        v_box.addWidget(self.button_plot)
        v_box.addWidget(self.button_save)
        v_box.addStretch(1)

        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        self._ax = self._fig.add_subplot(1, 1, 1)
        self._canvas: FigureCanvas = FigureCanvas(self._fig)
        self._canvas.setParent(self)

        h_box = qt.QHBoxLayout()
        h_box.addWidget(self._canvas, 1)
        h_box.addLayout(v_box)
        self.setLayout(h_box)

    @QtCore.pyqtSlot()
    def handle_click_on_button_plot(self) -> None:
        """
        Обработчик нажатия на кнопку 'Обновить фигуру'.
        """

        settings = {"freq_x": float(self.line_edit_freq_x.text()),
                    "freq_y": float(self.line_edit_freq_y.text()),
                    "phase_shift": float(self.line_edit_phase_shift.text()),
                    "resolution": int(self.line_edit_resolution.text()),
                    "color": COLOR_DICT[self.color_combobox.currentText()],
                    "width": int(self.combobox_width.currentText())}
        self.plot_lissajous_figure(settings)

    @QtCore.pyqtSlot()
    def handle_click_on_button_save(self) -> None:
        """
        Обработчик нажатия на кнопку 'Сохранить фигуру'.
        """

        filename, extension = qt.QFileDialog.getSaveFileName(self, "Сохранение изображения", DIR,
                                                             "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if extension == "PNG(*.png)":
            extension = "png"
        elif extension == "JPEG(*.jpg *.jpeg)":
            extension = "jpg"
        # Если не указано имя или расширение неверное, не сохраняем фигуру
        if filename == "" or extension not in ("png", "jpg"):
            return
        self._fig.savefig(filename, format=extension)

    def plot_lissajous_figure(self, settings: Dict[str, Union[float, str]] = DEFAULT_SETTINGS) -> None:
        """
        Метод рисует фигуру Лиссажу.
        """

        self._generator.set_resolution(settings["resolution"])
        figure = self._generator.generate_figure(settings["freq_x"], settings["freq_y"], settings["phase_shift"])
        self._ax.clear()
        self._ax.plot(figure.x_arr, figure.y_arr, color=settings["color"], linewidth=settings["width"])
        plt.axis("off")
        plt.tight_layout()
        self._canvas.draw()


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    main_window = LissajousWindow()
    main_window.show()
    sys.exit(app.exec_())
