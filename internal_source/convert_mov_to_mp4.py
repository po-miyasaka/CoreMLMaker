import argparse
import subprocess

def convert_mov_to_mp4(input_mov, output_mp4):
    command = f"ffmpeg -i {input_mov} -vcodec copy -acodec copy {output_mp4}"
    subprocess.run(command, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Convert a .mov video file to .mp4")
    parser.add_argument("input_mov", help="Path to the input .mov file")
    parser.add_argument("output_mp4", help="Path to the output .mp4 file")
    args = parser.parse_args()

    convert_mov_to_mp4(args.input_mov, args.output_mp4)

if __name__ == "__main__":
    main()
