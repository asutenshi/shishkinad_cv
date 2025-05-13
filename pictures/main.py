import cv2
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from pathlib import Path

"""При анализе изображений в видео, я обнаружил,
   что на моем изображении уникальное количество объектов - 15.
   Поэтому я просто проверял кол-во объектов на изображении,
   а затем вручную проверил, что все распознано правильно."""

capture = cv2.VideoCapture("output.avi")

# Использовал для сохранения всех изображений
# out_path = Path(__file__).parent / 'out'
# out_path.mkdir(exist_ok=True)

# Использовал для сохранения своего изображения
# my_image_path = Path(__file__).parent / 'my_images'
# my_image_path.mkdir(exist_ok=True)

# plt.figure()

count = 0
i = 1
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Бинаризацию и маркировку можно было сделать
    # средствами opencv, но мне привычнее уже работать с skimage
    thresh = threshold_otsu(gray)

    bin_image = gray < thresh

    labeled = label(bin_image)
    regions = regionprops(labeled)

    if len(regions) == 15:
        # Сохранение изображений для дебага
        # plt.cla()
        # plt.title(len(regions))
        # plt.imshow(frame)
        # plt.savefig(my_image_path / f'{i:05d}.png')
        count += 1

    i += 1

capture.release()
cv2.destroyAllWindows()

print(f"Количество моих изображений на видео: {count}")
