# -*- coding: utf-8 -*-
"""лаба2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gPW3P7gCiZATztWj8xPQrNcDA-T1J-C4
"""

from PIL import Image
import numpy as np
import math
import random

def halftone(image) :
  src = image.convert('RGB')
  image_arr = np.array(src)
  width, height = image.size
  new_image_arr = np.zeros(shape=(height, width))
  for x in range(width):
      for y in range(height):
          new_image_arr[y, x] = (image_arr[y, x, 0] + image_arr[y, x, 1] + image_arr[y, x, 2])/3
  new_image = Image.fromarray(new_image_arr.astype(np.uint8), 'L')
  return new_image

def lim(image_arr):
    bins = np.arange(np.min(image_arr) - 1, np.max(image_arr) + 1)
    hist, base = np.histogram(image_arr, bins=bins, density=True)
    base = base[1:].astype(np.uint8)
    w_0 = np.cumsum(hist)
    w_1 = np.ones(shape=w_0.shape) - w_0
    t_rank = 0
    i_max = 0
    for i, (w0, w1) in enumerate(zip(w_0, w_1)):
        m_0 = np.sum(base[:i] * hist[:i] / w0)
        m_1 = np.sum(base[i + 1:] * hist[i + 1:] / w1)
        d_0 = np.sum(hist[:i] * (base[:i] - m_0)**2)
        d_1 = np.sum(hist[i + 1:] * (base[i + 1:] - m_1)**2)
        d_all = w0 * d_0 + w1 * d_1
        d_class = w0 * w1 * (m_0 - m_1)**2
        if d_all == 0:
            i_max = i
            break
        if d_class / d_all > t_rank:
            t_rank = d_class / d_all
            i_max = i

    return base[i_max]

def findMean(matrix, t):
    data_ft = matrix.flatten()
    class_0 = data_ft[data_ft >= t]
    class_1 = data_ft[data_ft < t]
    if class_0.size > 0 :
      mean_1 = class_0.mean()
    else :
      mean_1 = 0
    if class_1.size > 0 :
      mean_2 = class_1.mean()
    else :
      mean_2 = 0
    return mean_1, mean_2

def pixel_change(image_arr, new_image_arr, x, y, l, L, a) :
  window_1 = image_arr[y:min(y + l, image_arr.shape[0]),
                         x:min(x + l, image_arr.shape[1])]
  window_2 = image_arr[max(y - L // 2 + 1, 0):min(y + L // 2 + l - 1, image_arr.shape[0]),
                        max(x - L // 2 + 1, 0):min(x + L // 2 + l - 1, image_arr.shape[1])]
  t = lim(window_2)
  m_0, m_1 = findMean(window_2, t)
  if math.fabs(m_0 - m_1) >= a :
      new_image_arr[y:min(y + l, image_arr.shape[0]),
                x:min(x + l, image_arr.shape[1])][window_1 > t] = 255
  else:
      central_pixel = window_1[window_1.shape[0] // 2, window_1.shape[1] // 2]
      if math.fabs(m_0 - central_pixel) < math.fabs(m_1 - central_pixel):
          new_image_arr[y:min(y + l, image_arr.shape[0]),
                    x:min(x + l, image_arr.shape[1])] = 255
  return new_image_arr

def Eikvel_binarization(image, l, L, a) :
  img = halftone(image)
  image_arr = np.array(img)
  new_image_arr = np.zeros(shape=image_arr.shape)
  x, y = 0, 0
  while y + l <= image_arr.shape[0]:
        if y % 2 == 0:
            while x + l < image_arr.shape[1]:
                new_image_arr = pixel_change(image_arr, new_image_arr, x, y, l, L, a)
                x += l
        else:
            while x - l > 0:
                new_image_arr = pixel_change(image_arr, new_image_arr, x, y, l, L, a)
                x -= l
        y += l

  new_image = Image.fromarray(new_image_arr.astype(np.uint8), 'L')
  return new_image

if __name__ == '__main__':



    with Image.open(f'im2.png').convert('RGB') as img:
        print(f'Opened image ')
        display(img)
        tmp1 = halftone(img)
        display(tmp1)
        print(f'Image  grayscale done')
        print(f'Starting binarizing')
        tmp2 = Eikvel_binarization(tmp1, 3, 15, 15)
        print(f'Image  done')
        display(tmp2)

"""время обработки 6 мин. 14 сек."""