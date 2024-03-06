## Tasks

This is a short interview coding task at Coram.AI for the software engineer candidates. We expect good fits to be fluent in both Python and C++ coding. This task mostly focuses on Python. C++ will be tested in subsequent interviews.

## Setup

1. Install [docker](https://docs.docker.com/engine/install/). Recommended version is `23.0.3`.
2. Run the code using `docker compose up --build`. Underhood, this command builds the docker image, launches the container, and executes the binaries for your test.
   - This setup has been tested on both Ubuntu and MacOS with M1 chips.

## Tasks

You need to implement the following services:

1. a "producer service" that loads a video and dumps images to a log folder at **15FPS**. There is a sample video in the `data` folder. You can use it for testing.
2. a "image processing service" that:

   - monitor the log folder and process images using the `classify_image` function in `src/utils` as soon as they are dumped to the folder.
     - `classify_image` uses a pre-trained ML model (ResNet101) to classify the image into one of the 1000 categories. Refer to [this](https://pytorch.org/hub/pytorch_vision_resnet/) for more details on ResNet and image classification.
     - Note that `src/utils` should be treated as a black box and you **SHOULD NOT** modify it.
   - publishes the results to the "states reporting service" below via pubsub
     - [pyzmq](https://github.com/zeromq/pyzmq) is a good library for pubsub messge passing and we have installed it in the docker image if you want to use it. Feel free to pick any other library you are familiar with though.
   - log throughput stats (e.g., number of images processed per second) to stdout

3. a "stats reporting service" that:

   - listen to the message queue and log detected class frequency to stdout every 10s. For example,

   ```
   In the past 10s:
   class 101 detected 11 times
   class 102 detected 5 times
   ```
