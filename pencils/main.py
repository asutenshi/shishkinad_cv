# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import sobel, threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing, binary_dilation
from collections import defaultdict

# %%

c = defaultdict(lambda: 0)
for i in range(1, 13):
    image = plt.imread(f'./images/img ({i}).jpg')[:, :, :-1].mean(axis=2)
    s = sobel(image)
    threshold = threshold_otsu(s)
    s[s < threshold] = 0
    s[s >= threshold] = 1
    # на многих изображениях карандаши не имели сплошного периметра,
    # поэтому применил наращивание
    for _ in range(5):
        s = binary_dilation(s)

    labeled = label(s)
    regions = regionprops(labeled)
    # сортировки для последующего вывода и оценивания характеристик карандашей 
    #regions = sorted(regions, key=lambda item: min(item.image.shape[0], item.image.shape[1]) / max(item.image.shape[0], item.image.shape[1]), reverse=True)
    #regions = sorted(regions, key=lambda item: item.perimeter)
    #regions = sorted(regions, key=lambda item: item.convex_area)
    #regions = sorted(regions, key=lambda item: item.eccentricity)

    # некоторые заметки подбора параметров
    # im2 = 0.0744, 23216, 63097/352793
    # im3 = 0.0720, 24188, 85389/421531
    # im4 = 0.0498, 17449, 44063/382669
    #       0.0581, 14245, 37757/418056
    # im5 = 0.4990, 20090, 55373/376490
    #       0.4300, 17125, 42252/370362
    # im9 = 0.8091, 20139, /431984
    # im11 = ... 0.9974, 0.9976, 0.9978
    # im12 = ... 0.9979

    for r in regions:
        # aratio = min(r.image.shape[0], r.image.shape[1]) / max(r.image.shape[0], r.image.shape[1])
        # per = r.perimeter
        c_area = r.convex_area
        ecc = r.eccentricity
        # Изначально сформировал условие по соотношению сторон, периметру и выпуклой площади,
        # а под конец пришла идея с эксцентритетом, но пришлось с помощью
        # выпуклой площади отсеять несколько объектов
        # if 0.0450 < aratio < 0.88 and 13000 < per < 40000 and 350000 < с_area < 525000:
        if 0.997 < ecc < 0.9985 and c_area > 20000:
            c[i] += 1

    # Вывод для поиска параметров в паре с сортировкой regions (сортировка выше)
    # for i in range(5):
    #     r = regions[-i]
    #     plt.figure(figsize=(8, 8))
    #     plt.imshow(r.image)
    #     aratio = min(r.image.shape[0], r.image.shape[1]) / max(r.image.shape[0], r.image.shape[1])
    #     per = r.perimeter
    #     с_area = r.convex_area
    #     plt.title(f'ratio = {aratio} \nper = {per} \nс_area = {с_area}')
    #     plt.show()
    #     print(aratio, per, area, c_area)

for k in range(1, 12):
    print(f'На изображении {k} находится {c[k]} карандашей')
print(f'Всего карандашей на изображениях {sum(c.values())}')
# %%
