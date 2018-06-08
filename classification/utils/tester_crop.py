from crop import crop, crop_pipeline
from os import listdir
from os.path import join, isfile
from matplotlib import pyplot as plt


def test_show_cropped_image(input):
    files = listdir(input)
    for f in files:
        img_path = join(input_path, f)
        if isfile(img_path):
            cropped = crop(img_path)
            plt.imshow(cropped)
            plt.show()


def test_create_cropped_pipeline(input, output):
    files = listdir(input)

    i = 0
    for f in files:
        img_path = join(input_path, f)
        if isfile(img_path):
            name = join(output, str(i) + ".png")
            crop_pipeline(img_path, name)


if __name__ == "__main__":
    input_path = './crop_single_test'
    output_path = './output'
    test_show_cropped_image(input_path)