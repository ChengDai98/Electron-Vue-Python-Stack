""" import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C:\\Users\\mnicd\\Documents\\CellDetectionSystem\\dgp\\90.bmp", 0)

f= np.fft.fft2(img)  # f是一个复数数组
fshift = np.fft.fftshift(f)
# fft_img = 20 * np.log(np.abs(fshift))

ishift = np.fft.ifftshift(fshift) #ishift是一个复数数组
i_img = np.fft.ifft2(ishift) #逆傅里叶变换，得到仍然是一个复数数组，不要以为直接得到图像的像素值.
i_img = np.abs(i_img) 


fig, ax = plt.subplots(1,2) #row = 1, col = 2

ax[0].imshow(img, cmap = "gray") 
ax[1].imshow(i_img, cmap = "gray")

ax[0].set_title("original"), ax[1].set_title("i_img")

ax[0].axis("off"), ax[1].axis("off")

# plt.savefig("result.jpg", dpi = 300, bbox_inches = "tight")
plt.show() """

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C:\\Users\\mnicd\\Documents\\CellDetectionSystem\\dgp\\2.15.png", 0)

dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
dftshift = np.fft.fftshift(dft)
# result = 20 * np.log(cv2.magnitude(dftshift[:,:, 0], dftshift[:, :, 1]))

idftshift = np.fft.ifftshift(dftshift)
idft = cv2.idft(idftshift)  #idft:二维复数数组
i_img = cv2.magnitude(idft[:, :, 0], idft[:,:, 1]) #转换到[0, 255]

fig, ax = plt.subplots(1,2) #row = 1, col = 2

ax[0].imshow(img, cmap = "gray") 
ax[1].imshow(i_img, cmap = "gray")

ax[0].set_title("original"), ax[1].set_title("i_img")

ax[0].axis("off"), ax[1].axis("off")

# plt.savefig("result.jpg", dpi = 300, bbox_inches = "tight")
plt.show()