# %%
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
from collections import defaultdict

# %%
# функция разделяющая оттенки
def shadesDivision(colors):
    sorted_colors = sorted(colors.items(), key=lambda item: item[0])
    d = np.diff([k for k, v in sorted_colors])
    pos = np.where(d > np.std(d)*2)
    splits = np.split(sorted_colors, pos[0]+1)
    shades = defaultdict(lambda: 0)
    for i, split in enumerate(splits):
        shade = round(np.mean(split[:, 0]), 2)
        shades[shade] = int(sum(split[:, 1]))
    return(shades)

image = plt.imread('balls_and_rects.png')
gray = image.mean(axis=2)
binary = gray > 0

labeled = label(binary)
regions = regionprops(labeled)

colors_rect = defaultdict(lambda: 0)
colors_circ = defaultdict(lambda: 0)
# 235 206 200 191 189 188 183 166 121 113 99 70 52 8 - все эти регионы
# имеют ecc = 0, но не являются кругами, поэтому отфильтрую по площади
for i, r in enumerate(regions):
    y, x = r.centroid
    hue = rgb2hsv(image[int(y), int(x)])[0]
    if r.area == r.image.shape[0]*r.image.shape[1]:
        # вывод для определения признаков
        # plt.figure()
        # plt.title(f'n = {i}\narea = {r.area}\na*b = {r.image.shape[0]*r.image.shape[1]}')
        # plt.imshow(r.image)
        # plt.show()
        colors_rect[hue] += 1
    else:
        colors_circ[hue] += 1

shades_rect = shadesDivision(colors_rect)
shades_circ = shadesDivision(colors_circ)
sorted_shades_rect = sorted(shades_rect.items(), key=lambda item: item[1])
sorted_shades_circ = sorted(shades_circ.items(), key=lambda item: item[1])


print(f'Всего фигур: {sum(colors_rect.values())+sum(colors_circ.values())}')
shades = shades_rect.keys() | shades_circ.keys()
for shade in shades:
    print(f'\tНа изображении {shades_rect[shade]+shades_circ[shade]} фигур оттенка {shade}')
print(f'Прямоугольников: {sum(colors_rect.values())}')
for k, v in sorted_shades_rect:
    print(f'\tНа изображении {v} прямоугольников оттенка {k}')
print(f'Кругов: {sum(colors_circ.values())}')
for k, v in sorted_shades_circ:
    print(f'\tНа изображении {v} кругов оттенка {k}')
# %%
