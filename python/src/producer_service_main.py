import argparse
import cv2
import os
import time
from datetime import datetime
import signal
import sys

def sigint_handler(signal, frame):
    print("SIGINT received. Exiting...")
    sys.exit(0)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file", type=str, required=True)
    parser.add_argument("--log_folder", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
    args = parse_args()
    dump_video(args.video_file, args.log_folder, 15)
    pass

def dump_video(video_file, log_folder, frame_rate):

    os.makedirs(log_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_file)

    frame_count = 0
    success = True

    while success:
        success, frame = cap.read()
        if frame is None:
            break

        epoch_time = int(time.time())

        output_path = os.path.join(log_folder, f'frame_{epoch_time}_{frame_count}.jpg')
        cv2.imwrite(output_path, frame)
        frame_count += 1
        time.sleep(1/15)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
