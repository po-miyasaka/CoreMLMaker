import sys
from pathlib import Path
sys.path.append(str(Path("internal_source").resolve()))

import convert_mov_to_mp4
import convert_video_to_images
import augmentation
import make_csv
import training

import argparse
from datetime import datetime
import os
import shutil
import config

def process(sources_path, should_make_dataset_only = False, foldername = ""):
    if should_make_dataset_only and foldername:
        print("-p and -n mustn't be used at the same time")
        return 
    # making a unique folder that contains all outputs of this process
    process_identifier =  foldername if foldername else datetime.now().strftime("%Y%m%d%H%M%S")
    makeDir("", "outputs")
    outputs_dir = os.path.join("outputs", process_identifier)
    mp4_dir, images_parent_dir, csv_dir, mlmodel_dir = [ makeDir(outputs_dir, name) for name in ["mp4", "images", "csv", "mlmodel"]]

    if not foldername:
        make_images(sources_path, images_parent_dir, mp4_dir)
        augment_images(images_parent_dir)

    if should_make_dataset_only:
        print(f"the folder name is {process_identifier}.")
        return
    
    # Making CSV that 
    csv_path = os.path.join(csv_dir, "data.csv")
    make_csv.make_csv(images_parent_dir, csv_path)

    # Making mlmodel
    mlmodel_path = os.path.join(mlmodel_dir, "ImageClassifier.mlmodel")
    training.export_mlmodel(csv_path, mlmodel_path)

# This function processes all files in the specified directory, converting them to .mp4 format and copying image files to an output folder. 
# The processing is performed recursively, including all nested directories and their files.
def make_images(sources_path, images_parent_dir, mp4_dir, images_dir_arg = "", nested = False):
        
    for item in os.listdir(sources_path):
        itemName, extension = os.path.splitext(item)
        lowered_extension = extension.lower()
        item_path = os.path.join(sources_path, item)
        images_dir = images_dir_arg if images_dir_arg else os.path.join(images_parent_dir, itemName)
        isImage = os.path.splitext(item)[1].lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        if (not nested) and (not isImage):
            os.makedirs(images_dir)

        if os.path.isdir(item_path):
            make_images(item_path, images_parent_dir, mp4_dir, images_dir_arg = images_dir,  nested = True)
        else:
            if lowered_extension.endswith('.mov'):
                video_path = os.path.join(mp4_dir, f"{itemName}.mp4")
                convert_mov_to_mp4.convert_mov_to_mp4(item_path, video_path)
                convert_video_to_images.extract_frames(video_path, images_dir, config.skip_frames)
            elif lowered_extension.endswith('.mp4'):
                video_path = os.path.join(mp4_dir, item)
                shutil.copy(item_path, video_path)
                convert_video_to_images.extract_frames(video_path, images_dir, config.skip_frames)
            else:
                if isImage:
                    shutil.copy2(os.path.join(sources_path, item), images_dir)
                else:
                    print(f"{item} is not a image file")


def augment_images(images_parent_dir):
    for folder in os.listdir(images_parent_dir):
        folder_path = os.path.join(images_parent_dir, folder)
        if os.path.isdir(folder_path):
            augmentation.batch_augmentation(folder_path) 

def makeDir(parentDir, childDirName):
    path = os.path.join(parentDir, childDirName)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("sources_path",  help="a folder that contains videos (MOV or mp4) that will convert to data set")
    parser.add_argument("-m", "--only-make-dataset", action="store_true", dest="should_make_dataset_only", help="only make datasets")
    parser.add_argument("-p", "--only-process-image-with-output-folder-id", dest="foldername", help="make mlmodel from prepared datasets that is spacified by foldernumber like 20230425074255")
    args = parser.parse_args()
    process(args.sources_path, args.should_make_dataset_only, args.foldername)

if __name__ == "__main__":
    main()
