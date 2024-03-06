## Tasks

This is a short C++ coding task at Coram.AI for the software engineer candidates.

## Setup

1. Install [docker](https://docs.docker.com/engine/install/). Recommended version is `23.0.3`.
2. Run the code using `docker compose up --build`. Underhood, this command builds the docker image, launches the container, and executes the binaries for your test.
   - This setup has been tested on both Ubuntu and MacOS with M1 chips.

## Tasks

You need to implement the following services under `src` folder:

1. a "producer service" that generates dummy image data at **15FPS** and dumps them to a log folder.
   - We have pre-installed [libtorch](https://pytorch.org/cppdocs/) in the docker image. Feel free to use it for your implementation.
   - It's recommended to use `/opt/logs` as the log folder. We have already configured it in docker-compose.yml so that it's mounted to the container.
2. a "image processing service" that:

   - monitor the log folder and process images using the `classifyImage` function in `src/image_processor_main.cc` as soon as they are dumped to the folder.
   - publishes the results to the "states reporting service" below via pubsub
     - [zeromq](https://zeromq.org/) is a good library for pubsub messge passing and we have installed it in the docker image if you want to use it. Feel free to pick any other library you are familiar with though.
   - log throughput stats (e.g., number of images processed per second) to stdout

3. a "stats reporting service" that:

   - listen to the message queue and log detected class frequency to stdout every 10s. For example,

   ```
   In the past 10s:
   class 101 detected 11 times
   class 102 detected 5 times
   ```

Extra requirements:

- Very likely "image processing service" can't process images as fast as they are dumped to the log folder as reported by the throughput stats. How to handle this situation? Please implement improvements to scale up the throughput as much as possible and report the throughput stats again. For example, use multi-threading to parallelize the image processing step.
