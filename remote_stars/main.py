import socket
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def color_region(region, im):
    minr, minc, maxr, maxc = region.bbox
    result = np.zeros_like(im)
    result[minr:maxr, minc:maxc] = im[minr:maxr, minc:maxc]
    return result

host = "84.237.21.36"
port = 5152

# Решение, которое я сделал на паре. Центроид отработает неправильно, если
# звезда будет расположена у края картинки. Также можно +- избавиться от сдвоенных звёзд
# путём повышения порога бинаризации

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     sock.connect((host, port))
#     beat = b"nope"

#     plt.ion()
#     plt.figure()

#     while beat != b"yep":
#         sock.send(b"get")
#         bts = recvall(sock, 40002)

#         im = np.frombuffer(bts[2:40002],
#                             dtype="uint8").reshape(bts[0], bts[1])
        
#         im[im < 1] = 0
#         im[im >= 1] = 1

#         labeled = label(im)
#         regions = regionprops(labeled)

#         if len(regions) < 2:
#             continue

#         pos1 = regions[0].centroid
#         pos2 = regions[1].centroid
#         result = round(np.sqrt((pos1[1] - pos2[1])**2 + (pos1[0] - pos2[0])**2), 1)

#         sock.send(f"{result}".encode())
#         print(f"test {result} : {sock.recv(10)}")

#         plt.clf()
#         plt.imshow(im)
#         plt.pause(1)

#         sock.send(b"beat")
#         beat = sock.recv(10)
#         print(f'beat : {beat}')

i = 1
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"

    plt.ion()
    plt.figure()

    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im = np.frombuffer(bts[2:40002],
                            dtype="uint8").reshape(bts[0], bts[1])
        
        binary = im.copy()
        # Не отрицаю, что даже при этом пороге звёзды могут срастись
        binary[binary < 30] = 0
        binary[binary >= 30] = 1

        labeled = label(binary)
        regions = regionprops(labeled)

        if len(regions) < 2:
            continue

        col_reg1 = color_region(regions[0], im)
        col_reg2 = color_region(regions[1], im)
        pos1 = np.unravel_index(np.argmax(col_reg1), col_reg1.shape) 
        pos2 = np.unravel_index(np.argmax(col_reg2), col_reg2.shape)
        # print(pos1, pos2)
        result = round(np.sqrt((pos1[1] - pos2[1])**2 + (pos1[0] - pos2[0])**2), 1)

        sock.send(f"{result}".encode())
        print(f"test{i} {result} : {sock.recv(10)}")

        plt.clf()
        plt.imshow(im)
        plt.pause(1)

        sock.send(b"beat")
        beat = sock.recv(10)
        print(f'beat{i} : {beat}')
        i += 1