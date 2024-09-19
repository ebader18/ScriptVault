import cv2
import numpy as np
import os

image_dir = 'C:/_sw/eb_python/photography/jpg/bill'
#image_dir = 'C:/_sw/eb_python/photography/jpg/cheese_knife'
#image_dir = 'C:/_sw/eb_python/photography/jpg/mug1'
#image_dir = 'C:/_sw/eb_python/photography/jpg/mug2'
#image_dir = 'C:/_sw/eb_python/photography/jpg/orange'
#image_dir = 'C:/_sw/eb_python/photography/jpg/pillow_heart'
#image_dir = 'C:/_sw/eb_python/photography/jpg/rock1'
#image_dir = 'C:/_sw/eb_python/photography/jpg/rock2'
#image_dir = 'C:/_sw/eb_python/photography/jpg/rock3'
#image_dir = 'C:/_sw/eb_python/photography/jpg/rock4'
#image_dir = 'C:/_sw/eb_python/photography/jpg/rock5'
#image_dir = 'C:/_sw/eb_python/photography/jpg/shoe'
#image_dir = 'C:/_sw/eb_python/photography/jpg/socket_driver'
#image_dir = 'C:/_sw/eb_python/photography/jpg/tea_storage'
#image_dir = 'C:/_sw/eb_python/photography/jpg/vice'


image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.JPG')]
image_files.sort()
images = [cv2.imread(file) for file in image_files]

exposure_times = np.array([1./50., 1./100, 1./200., 1./400., 1./800., 1./1600., 1./3200., 1./4000.], dtype=np.float32)

merge_debevec = cv2.createMergeDebevec()
hdr = merge_debevec.process(images, times=exposure_times.copy())

'''for gamma in range(1, 10, 1):
    tonemap = cv2.createTonemap(gamma=gamma)
    ldr = tonemap.process(hdr)

    # Convert to 8-bit and save
    ldr_8bit = np.clip(ldr*255, 0, 255).astype('uint8')
    cv2.imwrite(f'output_hdr_gamma_{gamma}.jpg', ldr_8bit)

    print("HDR image has been created and saved as 'output_hdr.jpg'.")
'''

'''gamma = 1.9
# for g in range(1, 20, 1):
# gamma = 1. + g/10.
for s in range(1, 20, 1):
    saturation = 0.5 + s/10.
    tonemap_drago = cv2.createTonemapDrago(gamma=gamma, saturation=saturation)
    ldr_drago = tonemap_drago.process(hdr)
    ldr_drago_8bit = np.clip(ldr_drago*255, 0, 255).astype('uint8')
    cv2.imwrite(f'output_hdr_gamma_{gamma}_saturation_{saturation}.jpg', ldr_drago_8bit)
'''

'''gamma = 1.9
intensity = 1
light_adapt = 0
for a in range(1, 10, 1):
    color_adapt = -5 + a
    tonemap_reinhard = cv2.createTonemapReinhard(gamma=gamma, intensity=intensity, light_adapt=light_adapt, color_adapt=color_adapt)
    ldr_reinhard = tonemap_reinhard.process(hdr)
    ldr_reinhard_8bit = np.clip(ldr_reinhard*255, 0, 255).astype('uint8')
    cv2.imwrite(f'output_hdr_gamma_{gamma}_intensity{intensity}_light_adapt{light_adapt}_color_adapt{color_adapt}.jpg', ldr_reinhard_8bit)'''

# for g in range(1, 20, 1):
gamma = 1.9
saturation = 1.3
tonemap_drago = cv2.createTonemapDrago(gamma=gamma, saturation=saturation)
ldr_drago = tonemap_drago.process(hdr)
ldr_drago_8bit = np.clip(ldr_drago*255, 0, 255).astype('uint8')
# cv2.imwrite(f'output_hdr_gamma_{gamma}_saturation_{saturation}.jpg', ldr_drago_8bit)

ldr_drago_8bit = cv2.resize(ldr_drago_8bit, (7008, 4672))
ldr_drago_8bit = cv2.rectangle(ldr_drago_8bit, (0, 0), (1920, 96), (255, 255, 255), -1)
cv2.putText(ldr_drago_8bit, f'hdr, gamma = {gamma}, saturation = {saturation}', (60, 72), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 0, 0), 3)

for i in range(8):
    images[i] = cv2.resize(images[i], (1752, 1168))
    images[i] = cv2.rectangle(images[i], (0, 0), (660, 96), (255, 255, 255), -1)
    cv2.putText(images[i], f'{exposure_times[i]:.5}s', (60, 72), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 0, 0), 3)

row1 = cv2.hconcat([images[0], images[1], images[2], images[3]])
row2 = cv2.hconcat([images[4], images[5], images[6], images[7]])
total = cv2.vconcat([row1, row2])
total = cv2.vconcat([total, ldr_drago_8bit])
cv2.imwrite(f'{os.path.basename(image_dir)}_gamma_{gamma}_saturation_{saturation}.jpg', total)
