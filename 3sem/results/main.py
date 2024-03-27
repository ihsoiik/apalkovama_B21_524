# -*- coding: utf-8 -*-
"""лаба3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZiEEbaLbtPbJKixExmUh7iQNoDsG48de
"""

import numpy as np
import math
from PIL import Image, ImageChops

def conservative_smoothing(image, filter_size):
    indexer = filter_size // 2
    new_image = image.copy()

    width, height = image.size
    pixels = new_image.load()

    for x in range(width):
        for y in range(height):
            window_values = []
            for i in range(max(0, x - indexer), min(width, x + indexer + 1)):
                for j in range(max(0, y - indexer), min(height, y + indexer + 1)):
                    if (i != x) or (j != y):
                        window_values.append(image.getpixel((i, j)))
            max_value = max(window_values)
            min_value = min(window_values)
            pixel_value = image.getpixel((x, y))
            if pixel_value > max_value:
                pixels[x, y] = max_value
            elif pixel_value < min_value:
                pixels[x, y] = min_value

    return new_image

def border(number_type, lower_border=None, upper_border=None):
    while True:
        try:
            number = number_type(input("Enter a number: "))
            if lower_border is not None and number < lower_border:
                raise ValueError(f"Number must be greater than {lower_border}")
            if upper_border is not None and number > upper_border:
                raise ValueError(f"Number must be less than {upper_border}")
            return number
        except ValueError as e:
            print(e)

def difference_image(image1, image2):
    assert image1.size == image2.size
    difference_image = ImageChops.difference(image1, image2)
    return difference_image

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

# Пример использования
image_path = 'lisa.png'
image = Image.open(image_path).convert('RGB')
images = halftone(image)

images

if __name__ == "__main__":
    k = border(int, 1)
    results = conservative_smoothing(images, k)
    results
    diff_images = difference_image(images, results)
    diff_images

results

diff_images = difference_image(images, results)
diff_images

image_path = 'im2.png'
image = Image.open(image_path).convert('RGB')
images = halftone(image)
images

if __name__ == "__main__":
    k = border(int, 1)
    results = conservative_smoothing(images, k)
    results
    diff_images = difference_image(images, results)
    diff_images

results

diff_images = difference_image(images, results)
diff_images