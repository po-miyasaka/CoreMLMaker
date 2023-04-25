import argparse
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
import cv2
import tensorflow as tf

def batch_augmentation(dir):
    list = os.listdir(dir)
    for filename in list:
        augmentation(dir, filename)

def augmentation(dir, filename):
    print(dir, filename)
    datagen = ImageDataGenerator(
        rotation_range=270,
        # width_shift_range=0.5,
        # height_shift_range=0.5,
        shear_range=np.random.uniform(0, 25),
        # zoom_range=0.7,
        # horizontal_flip=True,
        fill_mode='nearest',
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

    for _ in datagen.flow(x, batch_size=1, save_to_dir=dir, save_prefix=f"{os.path.splitext(filename)[0]}aug", save_format='jpeg'):
        i += 1
        if i > 10: 
            break
    os.remove(image_path)

def custom_preprocessing_function(image):
    contrast_factor = np.random.uniform(0.5, 1.5)
    brightness_factor = np.random.uniform(-40, 150)
    
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



# import argparse
# import cv2
# import numpy as np
# import os

# def adjust_brightness_contrast(image, alpha, beta):
#     return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# def augment_images(input_dir, output_dir):
#     # Create the output directory if it doesn't exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Read images from the input directory
#     for img_name in os.listdir(input_dir):
#         img_path = os.path.join(input_dir, img_name)
#         img = cv2.imread(img_path)

#         if img is None:
#             continue

#         # Save the original image
#         cv2.imwrite(os.path.join(output_dir, img_name), img)

#         # Define brightness and contrast adjustment values
#         adjustments = [
#             (1.0, 50),  # Increase brightness
#             (1.0, -50), # Decrease brightness
#             (1.5, 0),   # Increase contrast
#             (0.5, 0)    # Decrease contrast
#         ]

#         # Apply adjustments and save the augmented images
#         for i, (alpha, beta) in enumerate(adjustments):
#             augmented_img = adjust_brightness_contrast(img, alpha, beta)
#             output_path = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}_aug_{i}.jpg")
#             cv2.imwrite(output_path, augmented_img)

# def main():
#     parser = argparse.ArgumentParser(description="Convert a .mp4 to images")
#     parser.add_argument("input", help="images")
#     parser.add_argument("output", help="output")
#     args = parser.parse_args()

#     augment_images(args.input, args.output)

# if __name__ == "__main__":
#     main()