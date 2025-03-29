# %%
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import (binary_dilation, binary_erosion, 
                                binary_opening, binary_closing, disk)

# 1. Создаём простую бинарную маску
mask = np.zeros((10, 10), dtype=bool)
mask[2:8, 3:7] = True
mask[4, 5] = False  # "дырка"
mask[1, 1] = True   # "шум"

# 2. Задаём структурирующий элемент (например, круг)
selem = disk(1)

# 3. Применяем морфологические операции
dilated = binary_dilation(mask, selem)
eroded = binary_erosion(mask, selem)
opened = binary_opening(mask, selem)
closed = binary_closing(mask, selem)

# 4. Визуализация
titles = ['Original Mask', 'Dilation', 'Erosion', 'Opening', 'Closing']
images = [mask, dilated, eroded, opened, closed]

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()

# %%
