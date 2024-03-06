#!/bin/bash

# Fail on first error.
set -e

current_dir=$(pwd)
cd $current_dir/src

rm -rf build && mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=/usr/local/libtorch ..
cmake --build . --config Release
