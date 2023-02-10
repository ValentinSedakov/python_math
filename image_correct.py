import numpy as np
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('pic_mini.jpg')  # читаем изображение
gray = cv2.cvtColor(image,
                    cv2.COLOR_BGR2GRAY)  # оставляем монохромный вид, так как пока учусь работать с одним двумерным массивом
filtered = gray[:]
for y in range(1, gray.shape[0] - 1):  # Определяем границы обработки по у
    for x in range(1, gray.shape[1] - 1):  # по х
        filtered[y, x] = gray[y, x]

partsOfCube = [gray[
                   0, 0]] * 9  # создаем "матрицу" 3х3, в этой матрице будем искать среднее, можно и 5х5 назначить. Но вероятнее сильнее смажет.
for y in range(1, gray.shape[0] - 1):  # в границах изображения обрабатываем матрицы 3х3
    for x in range(1, gray.shape[1] - 1):
        partsOfCube[0] = gray[y - 1, x - 1]  # заполняем матрицу
        partsOfCube[1] = gray[y, x - 1]
        partsOfCube[2] = gray[y + 1, x - 1]
        partsOfCube[3] = gray[y - 1, x]
        partsOfCube[4] = gray[y, x]
        partsOfCube[5] = gray[y + 1, x]
        partsOfCube[6] = gray[y - 1, x + 1]
        partsOfCube[7] = gray[y, x + 1]
        partsOfCube[8] = gray[y + 1, x + 1]

        partsOfCube.sort()  # выбираем медиану
        filtered[y, x] = partsOfCube[4]

cv2.imshow('before filter', image)
cv2.imshow('after filter', filtered)
cv2.waitKey()

# gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
Fr = np.fft.fft2(filtered)  # раскладываем изображение в ряд Фурье
centering = np.fft.fftshift(Fr)  # Центрируем
centering = abs(centering)  # Для изображения оставляем только действительные составляющие
centering = np.log(centering + 1)  # Улучшем изображение гармоник
plt.imshow(centering)
plt.show()

mask = [[0, 0, 0],
        # Отчищаем изображение от бесполезных гармоник, увеличением яркости, оставляем только основные гармоники
        [0, 2, 0],
        [0, 0, 0]]

zeroMask = np.zeros(filtered.shape)
centX = filtered.shape[0] // 2
centY = filtered.shape[1] // 2
zeroMask[centX - 1: centX + 2, centY - 1: centY + 2] = mask
maskFr = np.fft.fft2(zeroMask)
Fr = Fr * maskFr
revers = np.fft.ifft2(Fr)
revers = abs(revers)

revers = np.append(  # Переставляем квадранты изображения, перепутанные из-за перемножения комплексных матриц
    revers[centX:, :],
    revers[:centX, :],
    axis=0)
revers = np.append(
    revers[:, centY:],
    revers[:, :centY],
    axis=1)
plt.imshow(revers)
plt.show()

cv2.imshow('out useful harmoni', revers / 255)  # Выводим результат без засветки
cv2.waitKey()

sobelX = cv2.Sobel(filtered, cv2.CV_64F, 1, 0,
                   ksize=3)  # Ищем границы отфильтрованногоизображения по собелю. Определяем градиенты по Х и У
sobelY = cv2.Sobel(filtered, cv2.CV_64F, 0, 1, ksize=3)  # k size - размер квадранта, которым "обрабатываем" изображение
absX = cv2.convertScaleAbs(
    sobelX)  # Преобразуем полученные границы в восьмибитные массивы, чтобы на картинке было что-то видно. Если оставим в исходном 16 битном виде, получим полную кашу
absY = cv2.convertScaleAbs(sobelY)
finGrad = cv2.addWeighted(absX, 0.5, absY, 0.5,
                          0)  # Добавляем наши границы с весом 0,5 (из-за величины объектов) в чб гамме

cv2.imshow('sobel', finGrad)
cv2.waitKey()

# границы по слоям:
image2 = cv2.imread('apple_pic.jpg')  # Разложим картинку с яблоками на цветовые слои
b = image2[:, :, 0]
g = image2[:, :, 1]
red = image2[:, :, 2]

sobelXb = cv2.Sobel(b, cv2.CV_64F, 1, 0, ksize=3)  # выделяем границы
sobelYb = cv2.Sobel(b, cv2.CV_64F, 0, 1, ksize=3)
absXb = cv2.convertScaleAbs(sobelXb)
absYb = cv2.convertScaleAbs(sobelYb)
Gradb = cv2.addWeighted(absXb, 0.5, absYb, 0.5, 0)

sobelXg = cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)
sobelYg = cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)
absXg = cv2.convertScaleAbs(sobelXg)
absYg = cv2.convertScaleAbs(sobelYg)
Gradg = cv2.addWeighted(absXg, 0.5, absYg, 0.5, 0)

sobelXred = cv2.Sobel(red, cv2.CV_64F, 1, 0, ksize=3)
sobelYred = cv2.Sobel(red, cv2.CV_64F, 0, 1, ksize=3)
absXred = cv2.convertScaleAbs(sobelXred)
absYred = cv2.convertScaleAbs(sobelYred)
Gradr = cv2.addWeighted(absXred, 0.5, absYred, 0.5, 0)

gr = cv2.merge((Gradb, Gradg, Gradr))  # собираем
cv2.imshow('Границы по слоям цветного изображения',
           gr)  # Получив границы цветов на их слоях, соединив их в одно целое, мы получили схему распределения/наличия цветов на картинке.
cv2.waitKey()
