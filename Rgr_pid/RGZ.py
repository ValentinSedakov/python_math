import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import CubicSpline

dt = 0.1
V = [1, 2]

RDots = np.array([np.arange(-4, 15, 1) * 5,
                  [0., 0., 0., 0., 0., 0., 8., 8., 3., 8., 2., 8., 4., 3., 0., 0., 0., 0.,
                   0.]])  # Задаём значения дороги

Road = CubicSpline(RDots[0, :], RDots[1, :])  # Интерполируем, приводим в "адекватный" графический вид

startData = [0., 0., 0]  # Стартовое положение и скорость
V = V[0]


# Отрисовка графика дороги
def Show_Graf(traectory, road_f):
    x_road = np.arange(0, 50, 0.01)
    y_road = road_f(x_road)

    fig, ax = plt.subplots(figsize=(8, 4),  # размер графика в дюймах
                           dpi=80,  # разрешение пикселей на дюйм
                           )
    plt.subplots_adjust(left=0.05, bottom=0.05,  # белые границы фигуры
                        right=0.95, top=0.95,
                        wspace=None, hspace=None)
    ax.set_ylim(-10, 20)
    ax.set_xlim(0, 50)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.plot(x_road, y_road, color='lightgrey', linewidth=40, alpha=0.8)
    ax.plot(x_road, y_road, color='orange', lw=3, ls='--', alpha=0.8)

    for car in traectory:
        ax.plot(car[0, :], car[1, :], color='red', linewidth=2, alpha=1)
        ax.plot(car[0, :], car[3, :], color='blue', linewidth=1, alpha=1)

    plt.show()


def distanse(x0, y0, f):
    """
    расстояние от точки до "дороги"
    положительные, если точка выше дороги
    отрицательное, если ниже
    """

    # минимизируемая функция
    def fn(x):
        return (f(x) - y0) ** 2 + (x - x0) ** 2

    # диапазон поиска
    def find_diap(a, b, fn):
        # первичный поиск диапазона перебором
        n_steps = 30  # число шагов поиска
        min_f = fn(a)
        min_i = 0
        step = (b - a) / n_steps
        for i in range(n_steps + 1):
            if fn(a + i * step) < min_f:
                min_f = fn(a + i * step)
                min_i = i

        b = a + min_i * step
        a = b - 2 * step
        return a, b

    # поиск методом деления попалам
    def minimize_half(a, b, fn):
        max_iter = 20  # предельное число итераций

        xm = (b + a) / 2
        for i in range(max_iter):
            f_xm = fn(xm)
            x1 = xm - (b - a) / 4
            f_x1 = fn(x1)
            x2 = xm + (b - a) / 4
            f_x2 = fn(x2)

            if f_x1 < f_xm:
                b = xm
                xm = x1
            elif f_x2 < f_xm:
                a = xm
                xm = x2
            elif f_x2 >= f_xm:
                a = x1
                b = x2
        return xm

    a, b = find_diap(x0 - 3, x0 + 3, fn)
    xm = minimize_half(a, b, fn)
    dist = math.sqrt(fn(xm))

    if y0 < f(x0):
        dist = -dist

    noize = 0.1 * (2 * np.random.rand() - 1)
    dist *= 1 - noize

    return [dist, xm, f(xm)]


def simulate_car(pilot_function, V, dt, start_data, road_function, max_X=50):
    """
    процесс расчета поездки по точкам
    """
    start_data.append(0.)
    car_data = np.array([start_data]).transpose()

    k = 0
    while car_data[0, -1] < max_X:
        k += 1

        dist = distanse(car_data[0, -1], car_data[1, -1], road_function)[0]

        alfa_now = pilot_function(dist)

        speed = V * dt  # скорость машинки
        x_car_now = car_data[0, -1] + speed * math.cos(alfa_now)
        y_car_now = car_data[1, -1] + speed * math.sin(alfa_now)

        car_data = np.array([
            np.append(car_data[0], x_car_now),
            np.append(car_data[1], y_car_now),
            np.append(car_data[2], alfa_now),
            np.append(car_data[3], dist)
        ])

        if k > 10000:
            print('предел обьема расчета')
            break

    return car_data


I = 0  # Переменная для хранения интегральной составляющей
pdelta = 0  # Переменная для хранения предыдущей дельты


def autoPilot(delta):
    delta = -delta  # минус нужен для того, чтобы машинка регулировалась к центру дороги (при новой дельте > предыдущей), а не уходила в кольцо.
    dt = 0.1  # Дискретность времени
    Kp = 4.53  # PID - коэффициенты
    Ki = 8.19
    Kd = 0.0183
    global I  # Глобализуем переменные, чтобы их можно было изменять в функции без инициализации
    global pdelta
    P = delta  # Рассчитываем составляющие
    I = I + delta * dt
    D = (delta - pdelta) / dt
    pdelta = delta  # Сохраняем данные о дельте
    CO = P * Kp + I * Ki + D * Kd

    return CO


car = []
car.append(simulate_car(autoPilot, V, dt, startData, Road, max_X=50))

Show_Graf(car, Road)
