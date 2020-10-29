"""
Usage:
    script_name.py (--input=input_path) (--output=output_path)
"""
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from docopt import docopt


def read_pdf(path):
    def convert_pil_to_cv(pil):
        open_cv_image = np.array(pil)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        return open_cv_image

    pages = convert_from_path(path, 500)
    return [convert_pil_to_cv(page) for page in pages]


def write_pdf(images, output_path):
    def convert_cv_to_pil(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)

    images = [convert_cv_to_pil(img) for img in images]
    images[0].save(output_path, save_all=True, append_images=images[1:])


def binarize(input_path, output_path):
    images = read_pdf(input_path)
    images = [cv2.GaussianBlur(img, (11, 11), 0) for img in images]
    images = [
        cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        for img in images
    ]
    write_pdf(images, output_path)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)

    binarize(arguments['--input'], arguments['--output'])

