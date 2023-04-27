import argparse
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
import cv2
import config
def batch_augmentation(dir):
    list = os.listdir(dir)
    for filename in list:
        augmentation(dir, filename)

def augmentation(dir, filename):
    print(dir, filename)
    datagen = ImageDataGenerator(
        rotation_range=config.rotation_range,
        width_shift_range=config.width_shift_range,
        height_shift_range=config.height_shift_range,
        shear_range=config.shear_range,
        zoom_range=config.zoom_range,
        horizontal_flip=config.horizontal_flip,
        fill_mode=config.fill_mode,
        preprocessing_function=custom_preprocessing_function
    )

    image_path = os.path.join(dir,filename)
    input_img = cv2.imread(os.path.join(dir,filename))
    resized_image = cv2.resize(input_img, (299, 299))
    color_fixed_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    normalized_image = color_fixed_image / 255.0
    x = img_to_array(normalized_image)
    x = np.expand_dims(x, axis=0)
    i = 0

    for _ in datagen.flow(x, batch_size=1, save_to_dir=dir, save_prefix=f"{os.path.splitext(filename)[0]}_aug", save_format='jpeg'):
        i += 1
        if i > 10: 
            break
    os.remove(image_path)

def custom_preprocessing_function(image):
    contrast_factor = config.contrast()
    brightness_factor = config.brightness()
    config.custom_image_fuction(image)
    """
    Adjust the exposure of an image using alpha (gain) and beta (bias).
    :param image: Input image
    :param alpha: Gain control (contrast)
    :param beta: Bias control (brightness)
    :return: Adjusted image
    """
    # float32 型から uint8 型に変換
    image = (image * 255).astype(np.uint8)

    # コントラストと明るさを調整
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_factor)

    # uint8 型から float32 型に変換し、[0, 1] の範囲にスケーリング
    adjusted_image = adjusted_image.astype(np.float32) / 255

    return adjusted_image

def main():
    parser = argparse.ArgumentParser(description="argumentation")
    parser.add_argument("input", help="input path")
    args = parser.parse_args()

    batch_augmentation(args.input)


if __name__ == "__main__":
    main()