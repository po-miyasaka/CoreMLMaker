import argparse
import os
import csv

def make_csv(parent_folder, output_csv_file):
    with open(output_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['image_path', 'label'])

        for filename in os.listdir(parent_folder):
            label, _ = os.path.splitext(filename)
            image_dir = os.path.join(parent_folder, label)
            if os.path.isdir(image_dir):
                for filename in os.listdir(image_dir):
                    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                        csv_writer.writerow([os.path.join(image_dir, filename), label])
def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("parent_folder", help="a folder that contains folders that contain images.")
    parser.add_argument("output_csv_file", help="csv path")
    args = parser.parse_args()

    make_csv(args.parent_folder, args.output_csv_file)

if __name__ == "__main__":
    main()