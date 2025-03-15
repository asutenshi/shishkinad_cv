import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_opening, 
                                binary_dilation, binary_erosion)

for i in range(1, 7):
    data = np.load(f'wires{i}npy.txt')
    labeled = label(data)
    print(f'Изначальное кол-во проводов: {np.max(labeled)}')
    plt.imshow(labeled)
    plt.show()

    for j in range(1, np.max(labeled) + 1):
        result = label(binary_erosion(labeled==j, np.ones(3).reshape(3, 1)))
        c = np.max(result)
        match c:
            case 0: print(f'{j} провод уничтожен')
            case 1: print(f'{j} провод цел')
            case _: print(f'{j} провод разрезан на {c} частей')
    print('')
