# usage: `python ~/Desktop/crop.py square_found.csv`
# assumes that images in current directory will be found and are the ones
# cropped into the output folder: cropped
# square_found.csv is generated by contours.py

import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
import pdb
import random as ra
import csv
import json
from lib.util import sort_coords
from lib.geom import skew

# Loading text data file
if len(sys.argv) > 1:
  filename = sys.argv[1]
else:
  print "No input data file given! \n"

if len(sys.argv) > 2:
  img_source_dir = sys.argv[2]
else:
  img_source_dir = '.'

with open(filename, 'rb') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    img_name,json_arr,s_height,s_width = row
    filename = img_source_dir + '/' + img_name
    s_height, s_width = [int(s_height), int(s_width)]
    landscape = s_width > s_height
    img = cv2.imread(filename,)
    l_height,l_width = img.shape[0:2]
    raw_coords = json.loads(json_arr)
    # raw_coords could be in any order, sort them...
    center_x = sum([p[0] for p in raw_coords]) / 4
    center_y = sum([p[1] for p in raw_coords]) / 4
    tl,bl,br,tr = sort_coords(raw_coords)

    # compute skew
    sides = [[tl[::-1], tr[::-1]], [tr, br], [br[::-1], bl[::-1]], [bl, tl]]
    avg_skew = sum([abs(skew(*s)) for s in sides]) / 4
    rotate_right = skew(*sides[0]) > 0 # negative first skew angle
    rotation_angle = (abs(avg_skew - 90) if rotate_right else avg_skew - 90)

    upw = lambda s: int(round(s * float(l_width) / s_width)) # scale up width
    uph = lambda s: int(round(s * float(l_height) / s_height)) # scale up height

    rot_mat = cv2.getRotationMatrix2D(center = (upw(center_x), uph(center_y)), angle = rotation_angle, scale = 1)
    rotated_img = cv2.warpAffine(src = img, M = rot_mat, dsize = (l_width,l_height), flags = cv2.INTER_CUBIC)

    wid, hei = [abs(tr[0] - tl[0]), abs(bl[1] - tl[1])]
    crop = cv2.getRectSubPix(image = rotated_img, patchSize = (upw(wid), uph(hei)), center = (upw(center_x), uph(center_y)))
    cv2.imwrite(img_source_dir + '/cropped/' + img_name, crop)
