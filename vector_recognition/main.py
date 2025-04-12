# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize
from skimage.segmentation import clear_border
from scipy.ndimage import convolve
from pathlib import Path
from collections import defaultdict

# %%
"""
Символ - сколько я распознал - сколько должно быть
/ 21 21
B 27 25
- 20 20
8 21 23
A 23 21
1 31 31
W 12 12
* 22 22
0 8  10
X 15 15
Неправильно распознано 8 символов. Ошибка < 5%
"""

def extractor(region):
    area = region.area / region.image.size
    width = region.image.shape[1]
    height = region.image.shape[0]
    cy, cx = region.centroid_local
    cy /= height
    cx /= width
    perimeter = region.perimeter / region.image.size
    eccentricity = region.eccentricity
    vlines = np.all(region.image, axis=0).sum() / region.image.shape[1]
    aspect_ratio = min(width, height) / max(width, height)
    h_area = hole_area(region) / region.image.size
    solidity = region.solidity
    euler_number = (region.euler_number - 1) / -2
#    circularity = (4 * np.pi * region.area) / (region.perimeter)**2
#    c_endpoints не сработал тк у эталонной звезды 9 конечных точек, а у тестовой 5
#    c_endpoints = count_endpoints(region.image)
#    c_endpoints = (c_endpoints - 0) / (9 - 0)
#    orientation = (region.orientation + np.pi / 2) / np.pi
    return np.array([area, cy, cx*10, perimeter, eccentricity*3,
                    vlines, aspect_ratio, h_area*1.5, solidity, euler_number])

def norm_l1(v1, v2):
    return ((v1 - v2)**2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result

def hole_area(region):
    inverted = ~region.image
    internal = clear_border(inverted)
    labeled = label(internal)
    regions = regionprops(labeled)
    return sum(region.area for region in regions)

"""
Эти функции я пробовал применять, но они не пригодились
"""
# def count_endpoints(binary):
#     skeleton = skeletonize(binary)
#     kernel = np.array([[1, 1, 1],
#                        [1, 0, 1],
#                        [1, 1, 1]])
#     neighbours = convolve(skeleton.astype(int), kernel, mode='constant', cval=0)
#     endpoints = (skeleton == 1) & (neighbours == 1)

#     return np.sum(endpoints)

# def count_junctions(binary):
#     skeleton = skeletonize(binary)
#     kernel = np.array([[1, 1, 1],
#                        [1, 0, 1],
#                        [1, 1, 1]])

#     neighbors = convolve(skeleton.astype(int), kernel, mode='constant', cval=0)
#     junctions = (skeleton == 1) & (neighbors >= 3)

#     return np.sum(junctions)

# def skeletion_length_ratio(binary):
#     skeleton = skeletonize(binary)
#     length = np.sum(skeleton)
#     area = np.sum(binary)
#     return length / area

image = plt.imread('alphabet-small.png')
image = image[:, :, :-1]
gray = image.mean(axis=2)
binary = gray < 1
labeled = label(binary)
regions = regionprops(labeled)

templates = {'A': extractor(regions[2]),
             'B': extractor(regions[3]), 
             '8': extractor(regions[0]),
             '0': extractor(regions[1]),
             '1': extractor(regions[4]),
             'W': extractor(regions[5]), 
             'X': extractor(regions[6]), 
             '*': extractor(regions[7]),
             '-': extractor(regions[9]), 
             '/': extractor(regions[8])}

# for k, v in templates.items():
#     print(k, v)

# Проверю правильно ли все распозналось
# c = 1
# for symbol, region in zip(templates, regions):
#     plt.subplot(2, 5, c)
#     plt.title(symbol)
#     plt.imshow(region.image)
#     c += 1

# Соотнесу индексы регионов с шаблонами
# for i, region in enumerate(regions):
#     v = extractor(region)
#     plt.subplot(2, 5, i+1)
#     plt.title(classificator(v, templates))
#     plt.imshow(region.image)

symbols = plt.imread('alphabet_ext.png')[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)


sym_count = defaultdict(lambda: 0)

"""
Для ручной проверки соответсвия распознавания
"""
# out_path = Path(__file__).parent / 'out'
# out_path.mkdir(exist_ok=True)
# plt.figure()
# for i, region in enumerate(regions):
#     v = extractor(region)
#     symbol = classificator(v, templates)
#     sym_count[symbol] += 1
#     plt.cla()
# #    plt.title(f'{symbol} {v}') # для дебага
#     plt.title(f'{symbol}')
#     plt.imshow(region.image)
#     plt.savefig(out_path / f'{i:03d}.png')
#     print(f'{i+1}/{len(regions)}')

for region in regions:
    v = extractor(region)
    symbol = classificator(v, templates)
    sym_count[symbol] += 1

for k, v in sym_count.items():
    print(k, v)
# %%
