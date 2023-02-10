import math
import matplotlib.pyplot as plt


def f(x):  # Исходная функция
    return (x - 5) ** 3 * math.cos(x)


# Находим значения ф-ции с шагом 0.1
x_dots = []
y_dots = []
for x in range(0, 101, 1):
    x_dots.append(0.1 * x)
for i in range(len(x_dots)):
    y_dots.append(f(x_dots[i]))

# Строим график
plt.plot(x_dots, y_dots)
# Построим прямую y=0, чтобы лучше видеть корни
ax = plt.gca()
ax.axhline(y=0, color='k')

plt.show()


# Визуально корни присутствуют на участках 1-2, 4-6, 7-8


def find_diap(f, x_min, x_max, dx):  # Поиск диапазона, в котором находятся корни
    rez = []
    x_a = x_min
    x_b = x_a + dx
    while x_a < x_max:
        if f(x_a) * f(x_b) <= 0: rez.append([x_a, x_b])
        x_a = x_b
        x_b = x_a + dx
    return rez


x_min = x_dots[0]
x_max = x_dots[-1]
dx = 0.1
k = find_diap(f, x_min, x_max, dx)
print(k)


# Результат [[1.5, 1.6], [4.7, 4.8], [5.0, 5.1], [7.8, 7.9]]


def find_root_half(f, diap, e):
    x_a = diap[0]
    y_a = f(x_a)

    x_b = diap[1]

    x_c = 0.5 * (x_a + x_b)
    y_c = f(x_c)

    k = 1
    while abs(y_c) >= e:
        if y_a * y_c <= 0:
            x_b = x_c
        else:
            x_a = x_c
            y_a = y_c
        x_c = 0.5 * (x_a + x_b)
        y_c = f(x_c)
        k += 1
    return x_c, y_c, k


print('Метод деления пополам')
for i in range(0, len(k)):  # Находим корни для каждого промежутка
    print(find_root_half(f, k[i], 0.1))


# Результат (1.56875, -0.08266692309881982, 4)
#          (4.749999999999999, -0.0005875336388746261, 1)
#          (5.049999999999998, 4.1404240029589146e-05, 1)
#          (7.849999999999988, 0.09217109904168976, 1)


def find_root_hord(f, diap, e):
    x_a = diap[0]
    x_b = diap[1]
    y_a = f(x_a)
    y_b = f(x_b)

    x_c = x_a - y_a * (x_b - x_a) / (y_b - y_a)

    y_c = f(x_c)
    X = [x_a, x_b, x_c]
    Y = [y_a, y_b, y_c]
    k = 3
    while abs(y_c) >= e:
        if y_c * y_a >= 0:
            x_a = x_c
            y_a = y_c
        else:
            x_b = x_c
            y_b = y_c

        x_c = x_a - y_a * (x_b - x_a) / (y_b - y_a)
        y_c = f(x_c)

        X.append(x_c)
        Y.append(y_c)
        k += 1
    return x_c, y_c, k  # ,X,Y


print('Метод Хорд')
for i in range(0, len(k)):  # Находим корни для каждого промежутка
    print(find_root_hord(f, k[i], 0.1))


# Результат (1.572547452296428, 0.07050686473480024, 3)
#          (4.732334317168701, -0.00038246408685461, 3)
#          (4.999999999999998, -1.5899815395065522e-45, 3)
#          (7.851354583353054, 0.060900607574927206, 3)


def find_root_tangent(f, diap, e):
    x1 = diap[1]
    x0 = diap[0]
    k = 0  # Счётчик итераций
    while True:  # Цикл с постусловием
        x2 = x1 - (x1 - x0) * f(x1) / (f(x1) - f(x0))  # Находим новую точку
        k += 1
        if abs(f(x2)) <= e:  # Проверяем значение в этой точке. Если значение <=e, эта точка - корень
            break;
        x1 = x2
    return x2, f(x2), k


print('Метод касательных')
for i in range(0, len(k)):  # Находим корни для каждого промежутка
    print(find_root_tangent(f, k[i], 0.1))


# Результат (1.572547452296428, 0.07050686473480024, 1)
#          (4.732334317168701, -0.00038246408685461, 1)
#          (4.999999999999998, -1.5899815395065522e-45, 1)
#          (7.851354583353054, 0.060900607574927206, 1)


def f_new(x):  # Функция для метода f'(x)=f(x)/(x-xi)
    y = (x - 5) ** 3 * math.cos(x)
    for m in range(0, i):  # делим ф-цию на (x-xi) для каждого найденного корня
        y = y / (x - X[m][0])
    return y


def find_root_f(f, f_new, diap, e):
    global X
    X = []  # Массив с корнями
    X.append(find_root_tangent(f, diap, e))  # Находим первый корень с помощью метода касательных
    global i  # Сделал X и i глобальными для упрощения работы с ф-циями
    for i in range(1, 4):  # Ищем оставшиеся корни, преобразуя ф-цию
        if X[i - 1][0] - diap[0] >= diap[1] - X[i - 1][
            0]:  # Метод касательных находит ближайший к краю диапазона корень
            diap[1] = X[i - 1][0] + 0.01  # Поэтому с каждым корнем уменьшаем диапазон, для меньшего числа итераций
        else:
            diap[0] = X[i - 1][0] - 0.01
        X.append(find_root_tangent(f_new, diap, e))  # Записываем корни в массив
    return X


print('метод f`(x)=f(x)/(x-xi)')
print(find_root_f(f, f_new, [0, 10], 0.1))
# Результат (1.572110703257283, 0.05294195958385367, 8)
#          (7.833898004841993, 0.07299066691653955, 2)
#          (5.3527732633745675, -0.0027964755024226075, 1)
#          (4.708633240468295, 1.4712923887903138e-05, 1)

