import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('C:\\Users\\mnicd\\Documents\\CellDetectionSystem\\dgp\\2.png', 0)
f = np.fft.fft2(img)

c = len(f)
cc = len(f[0])
sum = 0
sz = 0
for i in range(0, c):
    for j in range(0, cc):
        sum += abs(f[i][j])
        sz = sz + 1
sum = sum / sz
print(sum)

print(abs(f[0][0]))
print(len(f))
print(len(f[0]))

fshift = np.fft.fftshift(f)
print(fshift)
magnitude_spectrum = 20 * np.log(np.abs(fshift))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.savefig('240.png')
f1 = plt.figure()
plt.show()
