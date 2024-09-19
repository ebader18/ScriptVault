import numpy as np
import cv2
from fpdf import FPDF
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("--row", type=int,help="Number of rows")
ap.add_argument("--col", type=int,help="Number of columns")
ap.add_argument("--square_size", type=int,help="Square size in mm")
args = vars(ap.parse_args())

# Define the dimensions of the checkerboard
num_corners_x = args["col"]
num_corners_y = args["row"]
square_size_mm = args["square_size"]
checkerboard_width, checkerboard_height = num_corners_x * square_size_mm, num_corners_y * square_size_mm
fname = 'checkerboard_' + str(num_corners_x) + 'x' + str(num_corners_y) + '_' + str(square_size_mm) + 'mm'

# Generate the checkerboard image
checkerboard_img = np.zeros((checkerboard_height, checkerboard_width), dtype=np.uint8)
for i in range(num_corners_y):
    for j in range(num_corners_x):
        if (i + j) % 2 == 0:
            checkerboard_img[i * square_size_mm:(i + 1) * square_size_mm, j * square_size_mm:(j + 1) * square_size_mm] = 255

# Rotate the checkerboard image if needed so that the largest dimension is along the largest dimension of the PDF
if checkerboard_width > checkerboard_height:
    checkerboard_img = cv2.rotate(checkerboard_img, cv2.ROTATE_90_CLOCKWISE)
    checkerboard_height, checkerboard_width = checkerboard_width, checkerboard_height

pdf_height, pdf_width = 279.4, 215.9  # in mm
margin_x = (pdf_width - checkerboard_width) / 2
margin_y = (pdf_height - checkerboard_height) / 2

# Save the checkerboard image to a temporary PNG file
cv2.imwrite(fname + '.png', checkerboard_img)

# Save the image to a PDF file using fpdf
pdf = FPDF(unit='mm', format=(pdf_width, pdf_height))
pdf.add_page()
pdf.image(fname + '.png', x=margin_x, y=margin_y, w=checkerboard_width, h=checkerboard_height)
pdf.output(fname + '.pdf', 'F')

os.remove(fname + '.png')