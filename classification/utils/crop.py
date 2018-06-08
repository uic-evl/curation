import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
from geometry import contains, intersection, union


def dilate(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_dil = cv2.dilate(image, kernel, iterations=1)
    return img_dil


def merge_square_contours(cnts, width, height):
    """
    Merge overlapping contours. Only contours fully containing smaller contours are not merged.
    Processing each contour as a bounding box to perform union, contains and intersection operations.
    :param cnts: list of square contours
    :param width: width of the original image
    :param height: height of the original image
    :return: list of merged contours sorted by ranking
    """
    rects = []
    for cnt in cnts:
        rect = cv2.boundingRect(cnt)
        rects.append(rect)

    k = 0
    merged_squares = []

    while k < len(rects) - 1:
        if contains(rects[k], rects[k + 1]):
            merged_squares.append(rects[k])
            k += 1
        elif intersection(rects[k], rects[k + 1]) is not None:
            u = union(rects[k], rects[k+1])
            new_rect = list([u[0], u[1], u[2], u[3]])
            rects[k + 1] = new_rect
            k += 1
            if k == len(rects) - 1:
                merged_squares.append(new_rect)
        else:
            merged_squares.append(rects[k])
            k += 1
    if k == len(rects) - 1:
        merged_squares.append(rects[k])

    np_merged_squares = []
    # transform squares back to contours
    for msq in merged_squares:
        np_merged_squares.append(np.array(
            [[msq[0], msq[1]], [msq[0] + msq[2], msq[1]], [msq[0] + msq[2], msq[1] + msq[3]],
             [msq[0], msq[1] + msq[3]]]))
    sorted_merged_squares = sorted(np_merged_squares, key=lambda square: rank(square, width, height))
    return sorted_merged_squares


def get_contours(image):
    all_contours = []
    squares = []
    height = image.shape[0]
    width = image.shape[1]

    _, contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None

    for cnt in contours:
        all_contours.append(cnt)
        # only add bounding boxes (as contours) bigger than 20% of the image
        x, y, w, h = cv2.boundingRect(cnt)
        cnt = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
        if cv2.contourArea(cnt) / (width * height) > 0.2:
            squares.append(cnt)
        # if all the squares were too small, consider the whole image as the contour
        if len(squares) == 0:
            squares.append(np.array([[0, 0], [width, 0], [width, height], [9, height]]))

    # sorted_squares = sorted(squares, key=lambda square: rank(square, width, height))
    sorted_squares = sorted(squares, key=cv2.contourArea)
    max_area_contour = max(squares, key=cv2.contourArea)
    merged_squares = merge_square_contours(squares, width, height)

    return all_contours, sorted_squares, max_area_contour, merged_squares


# ranking of shapes
def rank(square, width, height):
    formatted = np.array([[s] for s in square], np.int32)
    x, y, wid, hei = cv2.boundingRect(formatted)
    max_distance_from_center = math.sqrt(((width / 2)) ** 2 + ((height / 2)) ** 2)
    distance_from_center = math.sqrt(((x + wid / 2) - (width / 2)) ** 2 + ((y + hei / 2) - (height / 2)) ** 2)

    height_above_horizontal = (height / 2) - y if y + hei > height / 2 else hei
    width_left_vertical = (width / 2) - x if x + wid > width / 2 else wid
    horizontal_score = abs(float(height_above_horizontal) / hei - 0.5) * 2
    vertical_score = abs(float(width_left_vertical) / wid - 0.5) * 2

    if cv2.contourArea(formatted) / (width * height) > 0.98:
        return 2  # max rank possible otherwise - penalize boxes that are the whole image heavily
    else:
        bounding_box = np.array([[[x, y]], [[x, y + hei]], [[x + wid, y + hei]], [[x + wid, y]]], dtype=np.int32)
        # every separate line in this addition has a max of 1
        return (distance_from_center / max_distance_from_center +
                cv2.contourArea(formatted) / cv2.contourArea(bounding_box) +
                cv2.contourArea(formatted) / (width * height) +
                horizontal_score +
                vertical_score)


def _crop(image_path):
    """
        Cropping the image based on the suggested pipeline by Ilya Kavalerov
        http://artsy.github.io/blog/2014/09/24/using-pattern-recognition-to-automatically-crop-framed-art/
        Not using pyramid expansion
    :param image_path: full path to the image to crop
    :return: cropped image
    """
    orig_img = cv2.imread(image_path)

    img_gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    img_dilated_1 = dilate(img_gray)
    img_blurred = cv2.medianBlur(img_dilated_1, 7)  # kernel_size = 7
    img_canny = cv2.Canny(img_blurred, threshold1=0, threshold2=55, apertureSize=3)
    img_dilated_2 = dilate(img_canny)
    all_contours, squares, max_square_contour, merged_squares = get_contours(img_dilated_2)

    x, y, w, h = cv2.boundingRect(merged_squares[0])
    output = orig_img[y:y+h, x:x+w]

    return output, orig_img, img_gray, img_dilated_1, img_blurred, img_canny, img_dilated_2, all_contours, squares, \
           max_square_contour, merged_squares


def crop(image_path):
    output, _, _, _, _, _, _, _, _, _, _ = crop(image_path)
    return output


def crop_pipeline(img_path, output_file_path):
    output, orig_img, img_gray, img_dilated_1, img_blurred, \
    img_canny, img_dilated_2, all_contours, squares, \
    max_square_contour, merged_squares = _crop(img_path)

    fig = plt.figure(figsize=(40, 20))
    plt.subplot2grid((2, 5), (0, 0)), plt.imshow(orig_img)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    plt.subplot2grid((2, 5), (0, 1)), plt.imshow(img_gray, cmap='gray')
    plt.title('Gray scale'), plt.xticks([]), plt.yticks([])

    plt.subplot2grid((2, 5), (0, 2)), plt.imshow(img_dilated_1, cmap='gray')
    plt.title('Dilated'), plt.xticks([]), plt.yticks([])

    plt.subplot2grid((2, 5), (0, 3)), plt.imshow(img_blurred, cmap='gray')
    plt.title('Median Filter'), plt.xticks([]), plt.yticks([])

    plt.subplot2grid((2, 5), (0, 4)), plt.imshow(img_canny)
    plt.title('Canny Edges'), plt.xticks([]), plt.yticks([])

    plt.subplot2grid((2, 5), (1, 0)), plt.imshow(img_dilated_2)
    plt.title('Dilated'), plt.xticks([]), plt.yticks([])

    img_with_all_contours = orig_img.copy()
    cv2.drawContours(img_with_all_contours, all_contours, -1, (255, 255, 0), 3)
    plt.subplot2grid((2, 5), (1, 1)), plt.imshow(img_with_all_contours)
    plt.title('All Contours'), plt.xticks([]), plt.yticks([])

    img_with_squares = orig_img.copy()
    cv2.drawContours(img_with_squares, squares, -1, (0, 255, 60), 3)
    plt.subplot2grid((2, 5), (1, 2)), plt.imshow(img_with_squares)
    plt.title('All Rectangles'), plt.xticks([]), plt.yticks([])

    img_with_merged_squares = orig_img.copy()
    cv2.drawContours(img_with_merged_squares, merged_squares, -1, (0, 255, 60), 3)
    plt.subplot2grid((2, 5), (1, 3)), plt.imshow(img_with_merged_squares)
    plt.title('Merged Squares'), plt.xticks([]), plt.yticks([])

    img_with_top_square = orig_img.copy()
    cv2.drawContours(img_with_top_square, [merged_squares[0]], -1, (0, 255, 60), 3)
    plt.subplot2grid((2, 5), (1, 4)), plt.imshow(img_with_top_square)
    plt.title('Top Ranked Shape'), plt.xticks([]), plt.yticks([])

    fig.savefig(output_file_path, dpi=fig.dpi)
    plt.close(fig)



#         # green = [0,255,0]
#         # pad = 10
#         # left_frame = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=green)
#         # h1, w1 = left_frame.shape[:2]
#         # h2, w2 = cropped.shape[:2]
#
#         # off_x = w1 - w2
#         # off_y = h1 - h2
#
#
#         # right_frame = cv2.copyMakeBorder(cropped, pad, off_y - pad, pad, off_x - pad, cv2.BORDER_CONSTANT, value=green)
#
#         # output_image = cv2.hconcat((left_frame, right_frame))
#         # cv2.imwrite(join(output_path, str(i) + ".jpg"), output_image)
#         # i = i + 1
#         # cv2.imshow('cropped ' + f , output_image)
#         # cv2.waitKey(0)
