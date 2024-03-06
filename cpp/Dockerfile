FROM jackcoram/coram-public-pytorch:latest

WORKDIR /opt/code

COPY . /opt/code
RUN ./install_zeromq.sh
RUN ./src/compile_binaries.sh
