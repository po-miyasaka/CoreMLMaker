import numpy as np
import turicreate


"""
Preferences of output images
"""
output_image_size = (299, 299)
width_shift_range = 0
height_shift_range = 0
zoom_range = 0.0
horizontal_flip = False
rotation_range = 270
shear_range = 25
fill_mode = 'nearest' # How to fill the space created by augmentation.
contrast = lambda: np.random.uniform(0.5, 1.5)
brightness = lambda: np.random.uniform(-40, 150)
custom_image_fuction = lambda image: image # image is 32 Float type


"""
Extract frames every this number of frame
"""
skip_frames = 15

"""
This function is called for training.
"""
training_function = lambda train_data, validation_data: turicreate.image_classifier.create(train_data, target='label', model='VisionFeaturePrint_Scene', validation_set=validation_data)