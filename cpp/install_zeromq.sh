#! /bin/bash

# Fail on first error.
set -e


CURRENT_DIR=$(pwd)
WORKING_DIR="/tmp/zeromq"
mkdir $WORKING_DIR && cd $WORKING_DIR

git clone --recursive https://github.com/zeromq/libzmq.git
cd libzmq
mkdir build
cd build
cmake ..
make -j4 install
cd ../
cp -a build /usr/local/libzmq

cd $WORKING_DIR
git clone --recursive https://github.com/zeromq/cppzmq.git
cd cppzmq
mkdir build
cd build
cmake ..
make -j4 install
cd ../
cp -a build /usr/local/cppzmq
