import cv2
import numpy as np
from cv2.typing import MatLike, Range

# read image as grayscale
img = cv2.imread("page1.jpg")
assert img is not None
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.jpg", gray)

# threshold
thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
shape = thresh.shape
kernel = np.ones((7, 7), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
kernel = np.ones((9, 9), np.uint8)
morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel)
cv2.imshow("morph", morph)
cv2.waitKey()
black_l = np.full(shape, 0)
black_r = np.full(shape, 0)
black_u = np.full(shape, 0)
black_d = np.full(shape, 0)
ans = []
for x in range(shape[0]):
    for y in range(shape[1]):
        if morph[x][y] != 0:
            black_l[x][y] = 0
            black_u[x][y] = 0
            continue
        if x > 1:
            black_l[x][y] = black_l[x - 1][y] + 1
        if y > 1:
            black_u[x][y] = black_u[x][y - 1] + 1

for x in reversed(range(shape[0])):
    for y in reversed(range(shape[1])):
        if morph[x][y] != 0:
            black_r[x][y] = 0
            black_d[x][y] = 0
            continue
        if x < shape[0] - 1:
            black_r[x][y] = black_r[x + 1][y] + 1
        if y < shape[1] - 1:
            black_d[x][y] = black_d[x][y + 1] + 1
        if (
            abs(black_l[x][y] - black_r[x][y]) < 5
            and abs(black_u[x][y] - black_d[x][y]) < 5
            and abs(black_u[x][y] - black_l[x][y]) < 5
        ):
            print(x, y)
            print(black_l[x][y], black_r[x][y])
            print(black_u[x][y], black_d[x][y])
            print("---")
            ans.append([y, x])
for p in ans:
    cv2.circle(morph, p, 5, [255, 0, 0], cv2.FILLED)
cv2.imshow("dots", morph)
cv2.waitKey()
# apply morphology
cv2.waitKey()
exit()

contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = contours[0] if len(contours) == 2 else contours[1]
area_thresh = 0
big_contour: MatLike | None = None
for c in contours:
    area = cv2.contourArea(c)
    if area > area_thresh:
        area_thresh = area
        big_contour = c

assert big_contour is not None
# get bounding box
x, y, w, h = cv2.boundingRect(big_contour)

# draw filled contour on black background
mask = gray.copy()
mask = cv2.merge([mask, mask, mask])
cv2.drawContours(mask, [big_contour], -1, (255, 0, 0), 5)
cv2.imshow("mask", mask)
cv2.waitKey()
