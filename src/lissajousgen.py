import numpy as np


class LissajousFigure:
    """
    Класс для фигуры Лиссажу. Задается набором точек с координатами x и y.
    """

    def __init__(self, x_array: np.ndarray, y_array: np.ndarray) -> None:

        self.x_arr: np.ndarray = x_array
        self.y_arr: np.ndarray = y_array


class LissajousGenerator:
    """
    Класс генерирует фигуры Лиссажу с заданными параметрами.
    """

    def __init__(self, resolution: int = 100) -> None:
        """
        :param resolution: количество точек.
        """

        self._resolution: int = None
        self.set_resolution(resolution)

    def generate_figure(self, freq_x: float, freq_y: float, phase_shift: float) -> LissajousFigure:
        """
        Метод генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        :param freq_x: частота колебаний по оси x;
        :param freq_y: частота колебаний по оси y;
        :param phase_shift: сдвиг фаз колебаний по осям x и y.
        :return: фигура Лиссажу - объект класса.
        """

        t = np.linspace(0, 2 * np.pi, self._resolution)
        x = np.sin(freq_x * t + phase_shift)
        y = np.sin(freq_y * t)
        return LissajousFigure(x, y)

    def set_resolution(self, resolution: int) -> None:
        """
        Метод задает количество точек в кривой.
        :param resolution: количество точек.
        """

        self._resolution = resolution
