path = strcat(pwd, '\data\liz_samples');
rgb_image = imread([path '\chicken1.jpg']);

[ features, cols, rows ] = get_descriptor(rgb_image);