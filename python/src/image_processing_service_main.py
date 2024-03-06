import argparse
import os
import time
from PIL import Image
import numpy as np
import zmq
import signal
import sys
import threading
import time
from utils import classify_image

def sigint_handler(signal, frame):
    print("SIGINT received. Exiting...")
    sys.exit(0)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_folder", type=str, required=True)
    return parser.parse_args()

def main() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
    args = parse_args()
    processor = image_processor()
    processor.init(args.log_folder)
    processor.process_new_files()

class image_processor:
    m_context = None
    m_socket = None
    m_log_folder = None
    m_images_processed = 0
    m_frame_mutex = None 


    def init(self, log_folder):
        self.m_context = zmq.Context()
        self.m_socket = self.m_context.socket(zmq.PUB)
        self.m_socket.bind("tcp://127.0.0.1:1234")
        self.m_log_folder = log_folder
        self.m_frame_mutex = threading.Lock()
        self.print_frames_processed()


    def print_frames_processed(self):
        frames = 0
        self.m_frame_mutex.acquire()
        frames = self.m_images_processed
        self.m_images_processed = 0
        self.m_frame_mutex.release()
        print("Frames processed per second", frames)
        threading.Timer(1, self.print_frames_processed).start()



    def process_new_files(self):
        
        initial_files = set(os.listdir(self.m_log_folder))

        while True:
            current_files = set(os.listdir(self.m_log_folder))
            new_files = current_files - initial_files
            initial_files = current_files

            for file_name in new_files:
                file_path = self.m_log_folder + "/" + file_name
                self.process_image(file_path)
                
    
    def process_image(self, file_name):
        #print(f"Processing File: {file_name}")

        if os.path.exists(file_name): 
            image = Image.open(file_name)
            image = image.resize((640, 360))
            image_array = np.array(image)

            if image_array.ndim == 2:
                image_array = np.stack((image_array,) * 3, axis=-1)
            elif image_array.shape[2] == 4:
                image_array = image_array[:, :, :3]

            retry_count, max_tries = 0, 3
            while retry_count < max_tries:
                try:
                    message_class = classify_image(image_array)
                    self.m_socket.send_pyobj(message_class)
                    self.m_frame_mutex.acquire()
                    self.m_images_processed += 1
                    self.m_frame_mutex.release()
                    break
                except zmq.error.ZMQError as e:
                    time.sleep(1/100)
                    retry_count += 1
            if retry_count == 3:
                print ("Unable to send classification message for image", file_name)

        else:
            print("File Not found", file_name)



if __name__ == "__main__":
    main()
