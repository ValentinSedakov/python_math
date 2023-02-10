import math
import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return (x - 5) ** 3 * math.cos(x)


x_dots = []
for new_x in range(0, 20, 2):
    x_dots.append(new_x)

y_dots = []
for i in range(len(x_dots)):
    new_y = f(x_dots[i])
    y_dots.append(new_y)


def find_part(x, X):
    if x < X[0]: return 1
    if x >= X[-1]: return len(X) - 1
    for i in range(len(x_dots) - 1):
        if X[i] <= x and x < X[i + 1]:
            return i + 1


x_real = [0.1 * x for x in range(185)]
y_real = [f(x) for x in x_real]
x_interp = x_real


def cube_interp(x, X, Y):
    # Находим участок (изменил find_part, чтобы мне было удобнее)
    i = find_part(x, X)
    # Выбираем 4 точки
    if i < 2:
        i = 2
    if i > len(X) - 2:
        i = len(X) - 2
    d0 = [x_dots[i - 2], y_dots[i - 2]]
    d1 = [x_dots[i - 1], y_dots[i - 1]]
    d2 = [x_dots[i], y_dots[i]]
    d3 = [x_dots[i + 1], y_dots[i + 1]]
    # Решаем систему для этих 4 точек, составив матрицу
    M = np.array(
        [[d1[0] ** 3, d1[0] ** 2, d1[0], 1], [d2[0] ** 3, d2[0] ** 2, d2[0], 1], [3 * d1[0] ** 2, 2 * d1[0], 1, 0],
         [3 * d2[0] ** 2, 2 * d2[0], 1, 0]])
    V = np.array([d1[1], d2[1], (d2[1] - d0[1]) / (d2[0] - d0[0]), (d3[1] - d1[1]) / (d3[0] - d1[0])])
    slv = np.linalg.solve(M, V)
    return slv[0] * x ** 3 + slv[1] * x ** 2 + slv[2] * x + slv[3]


y_cube_interp = [cube_interp(x, x_dots, y_dots) for x in x_interp]


def NutonK(X, Y):
    # Находим коэффициент A с помощью разделенных разностей
    f = [[0 for j in range(i + 1)] for i in range(len(X))]
    A = []
    for i in range(len(X)):
        for j in range(i + 1):
            if j == 0:
                f[i][j] = Y[i]
            else:
                f[i][j] = (f[j - 1][-1] - f[i][j - 1]) / (X[j - 1] - X[i])
            if i == j: A.append(f[i][j])
    return A


def p(x, X, Y, a):
    p = a[0]
    n = [1]

    def fN(x, X):
        for i in range(1, len(x_dots)):
            n.append((n[i - 1] * (x - X[i - 1])))
        return n

    n = fN(x, X)
    for i in range(1, len(a)):
        p = p + a[i] * n[i]
    return p


a = NutonK(x_dots, y_dots)
y_nuton = [p(x, x_dots, y_dots, a) for x in x_interp]

plt.scatter(x_dots, y_dots)  # Заданные точки
plt.plot(x_real, y_real, "red")  # Реальная ф-ция
plt.plot(x_interp, y_cube_interp)  # Кубическая интерполяция
plt.plot(x_interp, y_nuton)  # Интерполяция с помощью полинома Ньютона
plt.show()


# Рассчитываем погрешности
def find_error(y, Y):
    e = []
    for i in range(len(y)):
        if abs(Y[i]) <= 0.01:
            e.append((y[i] - Y[i]) * 100)  # Иначе при Y[i]~0, будет получатся бесконечность
        else:
            e.append((y[i] - Y[i]) / Y[i] * 100)
    return e


e_c = find_error(y_cube_interp, y_real)
e_n = find_error(y_nuton, y_real)

# Построим графики погрешности (Погрешность огромная в тех местах, где значение реальной функции близко к нулю)
plt.plot(x_real, e_n)
plt.plot(x_real, e_c)
plt.show()
