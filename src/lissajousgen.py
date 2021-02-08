import numpy as np


class Lissajous_figure:
    """Класс для фигуры Лиссажу. Задается набором точек с координатами
    x и y."""

    def __init__(self, x_array, y_array):

        self.x_arr = x_array
        self.y_arr = y_array


class Lissajous_generator:
    """Класс генерирует фигуры Лиссажу с заданными параметрами."""

    def __init__(self, resolution=100):
        self.set_resolution(resolution)

    def set_resolution(self, resolution: int):
        """Метод задает количество точек в кривой.
        :param resolution: количество точек."""

        self._resolution = resolution

    def generate_figure(self, freq_x: float, freq_y: float) -> Lissajous_figure:
        """Метод генерирует фигуру (массивы x и y координат точек) с заданными
        частотами.
        :param freq_x: частота колебаний по оси x;
        :param freq_y: частота колебаний по оси y.
        :return: фигура Лиссажу - объект класса."""

        t = np.linspace(0, 2 * np.pi, self._resolution)
        x = np.sin(freq_x * t)
        y = np.cos(freq_y * t)
        return Lissajous_figure(x, y)
