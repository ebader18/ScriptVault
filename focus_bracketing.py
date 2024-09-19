import cv2
import numpy as np
import os
import argparse


def load_and_align_images(image_paths):
    images = [cv2.imread(path) for path in image_paths]
    alignMTB = cv2.createAlignMTB()
    alignMTB.process(images, images)  # In-place modification of the list `images`
    return images


def measure_focus(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return laplacian.var()


def focus_stack(images):
    focus_measures = [measure_focus(img) for img in images]
    max_focus = np.max(focus_measures)
    best_idx = focus_measures.index(max_focus)
    return images[best_idx]


def main(image_dir, output_format):
    image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
    images = load_and_align_images(image_paths)
    stacked_image = focus_stack(images)
    output_file = os.path.join(image_dir, f'stacked_image.{output_format}')
    cv2.imwrite(output_file, stacked_image)
    cv2.imshow("Stacked Image", stacked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Focus stacking from images in a directory.')
    parser.add_argument('image_dir', type=str, help='Directory containing input images.')
    parser.add_argument('output_format', type=str, choices=['jpg', 'jpeg', 'png'], help='Output image format.')

    args = parser.parse_args()
    main(args.image_dir, args.output_format)
