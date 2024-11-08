mkdir build && cd ./build
mkdir output

export CC=gclang
export CXX=gclang++

CC=gclang CXX=gclang++ ../configure --prefix=$(pwd)/output
CC=gclang CXX=gclang++ make -j28 LDFLAGS="-latomic"

get-bc ./gdb/gdb