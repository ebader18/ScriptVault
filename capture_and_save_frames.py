import cv2
import argparse

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("--res", required=True, type=str, help="Camera resolution. Ex: 1280 720")
ap.add_argument("--source", required=True, type=str, help="Camera index, starts at 0")
ap.add_argument("--save_all", required=False, type=str, default="n", help="Save all images or only when key 's' is pressed? y or n")
ap.add_argument("--format", required=False, type=str, default="png", help="Output image format. Ex: png, jpg, bmp")
ap.add_argument("--split_horizontally", required=False, type=str, default="n", help="Split image horizontally in the middle? y or n")
args = vars(ap.parse_args())

# Extracting resolution and initializing variables
hres = int(args["res"].split()[0])
vres = int(args["res"].split()[1])
num = 0

# Set up the camera capture
cap = cv2.VideoCapture(int(args["source"]), cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, hres)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vres)

idx_img = 0
while cap.isOpened():
    succes, img = cap.read()
    # img = cv2.flip(img, 1)
    k = cv2.waitKey(1)

    if k == 27 or k == ord('q'):
        break
    elif args["save_all"] == 'y' or k == ord('s'):  # wait for 's' key to save
        if args["split_horizontally"] == 'y':
            mid = hres // 2
            right_img = img[:, :mid]  # Left half
            left_img = img[:, mid:]  # Right half
            cv2.imwrite(f'left_image_{idx_img:05d}.{args["format"]}', left_img)
            cv2.imwrite(f'right_image_{idx_img:05d}.{args["format"]}', right_img)
        else:
            cv2.imwrite(f'image_{idx_img:05d}.{args["format"]}', img)
        idx_img += 1

    cv2.imshow('Img', img)

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
