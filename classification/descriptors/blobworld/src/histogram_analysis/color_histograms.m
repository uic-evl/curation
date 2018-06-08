path = 'D:\udel\part2_for_sharing_03222018\Fluorescence\test\';
img_name = '8707857_4_P1.bmp';

img = imread(strcat(path,img_name));

r = img(:,:,1);
g = img(:,:,2);
b = img(:,:,3);

[yR, x] = imhist(r);
[yG, x] = imhist(g);
[yB, x] = imhist(b);

plot(x, yR, 'Red', x, yG, 'Green', x, yB, 'Blue');
