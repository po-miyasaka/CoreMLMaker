import os
import turicreate as tc
import argparse
import config

def export_mlmodel(csv_path, mlmodel_path):
    data = tc.SFrame.read_csv(csv_path)
    data['image'] = data['image_path'].apply(lambda path: tc.Image(path))
    
    train_data, validation_data = data.random_split(0.8, seed=42)
    model = config.training_function(train_data, validation_data)
    accuracy = model.evaluate(validation_data)['accuracy']
    print("Accuracy: ", accuracy)

    model.export_coreml(mlmodel_path)

    ios_sample_dir = os.path.join("iOSSample", "ImageMatching", "ImageClassifier.mlmodel")
    if os.path.exists(ios_sample_dir):
        model.export_coreml(ios_sample_dir)

def main():
    parser = argparse.ArgumentParser(description="training")
    parser.add_argument("csv_path", help="a directory that the csv will be saved in")
    parser.add_argument("mlmodel_path", help="a directory that the mlmodel will be saved in")
    args = parser.parse_args()

    export_mlmodel(args.csv_path, args.mlmodel_path)

if __name__ == "__main__":
    main()