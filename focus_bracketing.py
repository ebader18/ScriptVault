import cv2
import numpy as np
import os


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


image_dir = 'C:/_sw/eb_python/photography/focus_bracketing/jpg'
image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.JPG')]
images = load_and_align_images(image_paths)
stacked_image = focus_stack(images)
cv2.imwrite(f'{image_dir}/stacked_image.jpg', stacked_image)
# cv2.imshow("Stacked Image", stacked_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
