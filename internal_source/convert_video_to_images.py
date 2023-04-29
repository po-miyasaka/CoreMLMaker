import cv2
import os
import argparse
import config

def extract_frames(video_path, output_dir, skip_frames):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Load the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return

    frame_count = 0
    saved_count = 0

    while True:
        # Read the next frame from the video
        ret, frame = cap.read()

        # Break the loop if we have reached the end of the video
        if not ret:
            break

        # Save the frame as an image every 'skip_frames' frames
        if frame_count % skip_frames == 0:
            # Save the frame as an image
            output_path = os.path.join(output_dir, f"{video_name}_frame_{frame_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1

        frame_count += 1

    # Release the video file and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    print(f"Extracted {saved_count} frames from the video.")

# Example usage

def main():
    parser = argparse.ArgumentParser(description="Convert a .mp4 to images")
    parser.add_argument("input", help="Path to the input mp4")
    parser.add_argument("output", help="Path to the images output")
    args = parser.parse_args()

    extract_frames(args.input, args.output, config.skip_frames)

if __name__ == "__main__":
    main()
