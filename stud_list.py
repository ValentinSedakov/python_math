import numpy as np
import sys


def group_gener():
    names = ['Александр', 'Борис', 'Владимир', 'Геннадий', 'Дмитрий', 'Егор', 'Жангиз', 'Захар']

    def one_fate():
        r = [np.random.randint(0, len(names)) for x in range(3)]
        name = (names[r[0]][:-1] + 'ев',
                names[r[1]],
                names[r[2]] + 'ович')
        table = []
        for i in range(3):
            table.append([])
            for j in range(5):
                table[i].append(np.random.randint(3, 6))
        return [name, table]

    group = {i + 1: one_fate() for i in range(10)}
    return group


def print_group_list():
    print('Список студентов')
    for key in group:
        print(key,
              group[key][0][0],
              group[key][0][1],
              group[key][0][2])


def print_selected_student():
    print('введите номер студента или введите quit для выхода:',
          end=' ')  # Добавил возможность выхода, без просмотра оценок одного из студентов
    try:
        n = input()
        if n == 'quit':
            sys.exit  # Нашёл такой способ завершения программы
        else:
            print_student(n), data_correction(n)  # Выводятся данные студента и запускается функция для изменения данных
    except:
        print('Ошибка ввода 1')


def data_correction(n):  # Ф-ция для изменения оценок за семестр
    print('введите 0 - для того, чтобы вернуться назад; 1 - для изменения данных:', end=' ')
    try:
        t = int(input())
        while True:  # Сделал цикл, для возможности преждевременного выхода из условия if (Наверняка есть более адекватный вариант для реализации этого)
            if t == 0:
                break
            elif t == 1:
                print('введите номер семестра:', end=''),
            try:
                k = int(input()) - 1  # k - номер семестра
                for i in range(5):  # Цикл для ввода каждой оценки за семестр
                    print('введите', i + 1, 'оценку:', end='')
                    group[int(n)][1][k][i] = int(input())
                print_mid_table()
                print_selected_student()
            except:
                print('Ошибка 2')
            break
    except:
        print('Ошибка ввода 3')
    print_mid_table()
    print_selected_student()


def print_student(n):
    student = group.get(int(n))
    for x in student[0]:
        print(x, end=' ')
    print()
    for i in range(len(student[1])):
        print(i + 1, "семестр:", end=' ')
        for j in student[1][i]:
            print(j, end=' ')
        print()


def print_mid_table():
    for key in group:
        string = str(key) + ' ' \
                 + group[key][0][0] + ' ' \
                 + group[key][0][1][0] + '. ' \
                 + group[key][0][2][0] + '. '
        mid_count = []
        for semestr in group[key][1]:
            mid_count.append(sum(semestr) / len(semestr))
        better = True
        for i in range(len(mid_count) - 1):
            if mid_count[i] >= mid_count[i + 1]: better = False
        mid_count = round(sum(mid_count) / len(mid_count), 1)
        string += ' Средний балл: ' + str(mid_count)
        if better: string += ' Улучшил успеваемость'
        print(string)


group = group_gener()
print_mid_table()
print_selected_student()
