import numpy as np
import cv2
import random
import math
from os import listdir
from os.path import join, isfile
from matplotlib import pyplot as plt

# https://code.google.com/p/pythonxy/source/browse/src/python/OpenCV/DOC/samples/python2/squares.py?spec=svn.xy-27.cd6bf12fae7ae496d581794b32fd9ac75b4eb366&repo=xy-27&r=cd6bf12fae7ae496d581794b32fd9ac75b4eb366
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def dilate(image):
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	img_dil = cv2.dilate(image, kernel, iterations=1)
	return img_dil

def blur(image, kernel_size):
	img_blur = cv2.medianBlur(image, kernel_size)
	return img_blur

def canny(image):
	img_canny = cv2.Canny(image, threshold1 = 0, threshold2 = 55, apertureSize = 3)
	return img_canny

def get_max_bounding_box(image, output):
	all_contours = []
	squares = []
	height = image.shape[0]
	width = image.shape[1]

	img_copy = image.copy()
	_, contours, _ = cv2.findContours(img_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) != 0:
	    for cnt in contours:
	      all_contours.append(cnt)
	      cnt_len = cv2.arcLength(cnt, True)
	      x, y, w, h = cv2.boundingRect(cnt)
	      cnt = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
	      if cv2.contourArea(cnt) > (width * height/5):
	      	squares.append(cnt)
	    # cuts were too small. Most likely is a full image
	    if len(squares) == 0:
	    	squares.append(np.array([[0, 0], [width, 0], [width, height], [9, height]]))
	else:
		return None
	
	#debug = False
	#if debug:
	#	output_copy = output.copy()
		
	#	if len(contours) != 0:
	#		cv2.drawContours(output_copy, contours, -1, (255,255,0), 3)
	#		for contour in contours:
	#			rect = cv2.boundingRect(contour)
	#			cv2.rectangle(output_copy, (rect[0], rect[1]), (rect[2]+rect[0],rect[3]+rect[1]), (0,255,0), 2)
	#		cv2.rectangle(output_copy,(c_x,c_y),(c_x+c_w, c_y + c_h),(0,0,255),2)
	#		debug_view('contours', output_copy, True)

	#sorted_squares = sorted(squares, key=lambda square: rank(square, width, height))
	sorted_squares = sorted(squares, key=cv2.contourArea)
	max_area_contour = max(squares, key = cv2.contourArea)

	return all_contours, sorted_squares, max_area_contour

# ranking of shapes
def rank(square, width, height):
  formatted = np.array([[s] for s in square], np.int32)
  x,y,wid,hei = cv2.boundingRect(formatted)
  max_distance_from_center = math.sqrt(((width / 2))**2 + ((height / 2))**2)
  distance_from_center = math.sqrt(((x + wid / 2) - (width / 2))**2 + ((y + hei / 2) - (height / 2))**2)

  height_above_horizontal = (height / 2) - y if y + hei > height / 2 else hei
  width_left_vertical = (width / 2) - x if x + wid > width / 2 else wid
  horizontal_score = abs(float(height_above_horizontal) / hei - 0.5) * 2
  vertical_score = abs(float(width_left_vertical) / wid - 0.5) * 2

  if cv2.contourArea(formatted) / (width * height) > 0.98:
    return 2 # max rank possible otherwise - penalize boxes that are the whole image heavily
  else:
    bounding_box = np.array([[[x,y]], [[x,y+hei]], [[x+wid,y+hei]], [[x+wid,y]]], dtype = np.int32)
    # every separate line in this addition has a max of 1
    return (distance_from_center / max_distance_from_center +
      cv2.contourArea(formatted) / cv2.contourArea(bounding_box) +
      cv2.contourArea(formatted) / (width * height) + 
      horizontal_score + 
      vertical_score)

def union(a,b):
	x = min(a[0], b[0])
	y = min(a[1], b[1])
	w = max(a[0]+a[2], b[0]+b[2]) - x
	h = max(a[1]+a[3], b[1]+b[3]) - y
	return (x, y, w, h)

def intersection(a,b):
	x = max(a[0], b[0])
	y = max(a[1], b[1])
	w = min(a[0]+a[2], b[0]+b[2]) - x
	h = min(a[1]+a[3], b[1]+b[3]) - y
	if w<0 or h<0: return None
	return (x, y, w, h)

def contains(a, b):
	x, y, w, h = union(a, b)
	if (x == a[0] and y == a[1] and w == a[2] and h == a[3]) or (x == b[0] and y == b[1] and w == b[2] and h == b[3]):
		return True
	else:
		return False

def remove_background(img_path, output_path):
	img = cv2.imread(img_path)

	output = img.copy()
	height = img.shape[0]
	width = img.shape[1]

	fig = plt.figure(figsize=(40,20))
	plt.subplot2grid((2,5), (0,0)),plt.imshow(img)
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])

	# Process the image in grayscale color space
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#debug_view('gray_scale', img_gray, debug)
	plt.subplot2grid((2,5), (0,1)),plt.imshow(img_gray, cmap='gray')
	plt.title('Grayscale'), plt.xticks([]), plt.yticks([])
	
	img_dil = dilate(img_gray)
	plt.subplot2grid((2,5), (0,2)),plt.imshow(img_dil, cmap='gray')
	plt.title('Dilated'), plt.xticks([]), plt.yticks([])
	
	img_blur = blur(img_dil, 7)
	plt.subplot2grid((2,5), (0,3)),plt.imshow(img_blur, cmap='gray')
	plt.title('Median Filter'), plt.xticks([]), plt.yticks([])
	
	# Not using resizing. Tests showed that it was not helpful
	#small = cv2.pyrDown(img_blur, dstsize=(int(width/2), int(height/2)))
	#oversized = cv2.pyrUp(small, dstsize=(width, height))

	img_canny = canny(img_blur)
	plt.subplot2grid((2,5), (0,4)),plt.imshow(img_canny)
	plt.title('Canny Edges'), plt.xticks([]), plt.yticks([])
	
	img_dil2 = dilate(img_canny)
	plt.subplot2grid((2,5), (1,0)),plt.imshow(img_dil2)
	plt.title('Dilated'), plt.xticks([]), plt.yticks([])

	contours, squares, max_square_contour = get_max_bounding_box(img_dil2, output)
	img_with_all_contours = img.copy()
	cv2.drawContours(img_with_all_contours, contours, -1, (255,255,0), 3)
	plt.subplot2grid((2,5), (1,1)),plt.imshow(img_with_all_contours)
	plt.title('All Contours'), plt.xticks([]), plt.yticks([])

	img_with_squares = img.copy()
	cv2.drawContours(img_with_squares, squares, -1, (0,255,60), 3)
	plt.subplot2grid((2,5), (1,2)),plt.imshow(img_with_squares)
	plt.title('All Rectangles'), plt.xticks([]), plt.yticks([])

	rects = []
	for square in squares:
		rect = cv2.boundingRect(square)
		rects.append(rect)
	i = 0
	merged_squares = []

	while i < len(rects) - 1:
		if contains(rects[i], rects[i+1]):
			merged_squares.append(rects[i])
			i = i + 1
		elif intersection(rects[i],rects[i+1]) is not None:
			#rectList, _ = cv2.groupRectangles([rects[i], rects[i+1]], 1, 0)
			x = min(rects[i][0], rects[i+1][0])
			y = min(rects[i][1], rects[i+1][1])
			w = max(rects[i][0] + rects[i][2], rects[i+1][0] + rects[i+1][2]) - x
			h = max(rects[i][1] + rects[i][3], rects[i+1][1] + rects[i+1][3]) - y

			rects[i + 1] = list([x, y, w, h])
			print(rects[i+1])
			i = i + 1
			if i == len(rects) - 1:
				merged_squares.append(list([x, y, w, h]))
		else:
			merged_squares.append(rects[i])
			i = i + 1
	if i == len(rects) - 1:
		merged_squares.append(rects[i])

	np_merged_squares = []
	for msq in merged_squares:
		np_merged_squares.append(np.array([[msq[0], msq[1]], [msq[0] + msq[2], msq[1]], [msq[0] + msq[2], msq[1] + msq[3]], [msq[0], msq[1] + msq[3]]]))
	sorted_merged_squares = sorted(np_merged_squares, key=lambda square: rank(square, width, height))


	img_with_merged_squares = img.copy()
	cv2.drawContours(img_with_merged_squares, np_merged_squares, -1, (0,255,60), 3)
	plt.subplot2grid((2,5), (1,3)),plt.imshow(img_with_merged_squares)
	plt.title('Merged Squares'), plt.xticks([]), plt.yticks([])

	img_with_top_square = img.copy()
	cv2.drawContours(img_with_top_square, [sorted_merged_squares[0]], -1, (0,255,60), 3)
	plt.subplot2grid((2,5), (1,4)),plt.imshow(img_with_top_square)
	plt.title('Top Ranked Shape'), plt.xticks([]), plt.yticks([])

	fig.savefig(output_path, dpi=fig.dpi)
	plt.close(fig)
	#plt.show()
	#x, y, w, h = cv2.boundingRect(squares[0])

	#if x is not None:
	#	crop_img = img[y:y+h, x:x+w]
	#else:
	#	crop_img = output

	#return img, crop_img

input_path = './input'
#input_path = 'D:/udel/part1_for_sharing_03222018/Microscopy'
output_path = './output'
files = listdir(input_path)

i = 0
for f in files:
	img_path = join(input_path, f)
	if isfile(img_path):
		#img, cropped = remove_background(img_path, False)
		name = join(output_path, str(i) + ".png")
		print(f)
		remove_background(img_path, name)
		i = i + 1
		#green = [0,255,0]
		#pad = 10
		#left_frame = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=green)
		#h1, w1 = left_frame.shape[:2]
		#h2, w2 = cropped.shape[:2]

		#off_x = w1 - w2
		#off_y = h1 - h2


		#right_frame = cv2.copyMakeBorder(cropped, pad, off_y - pad, pad, off_x - pad, cv2.BORDER_CONSTANT, value=green)

		#output_image = cv2.hconcat((left_frame, right_frame))
		#cv2.imwrite(join(output_path, str(i) + ".jpg"), output_image)
		#i = i + 1
		#cv2.imshow('cropped ' + f , output_image)
		#cv2.waitKey(0)