export LLVM_COMPILER=clang

make clean

export CC=gclang
export CXX=gclang++

make

get-bc src/redis-server
get-bc src/redis-cli
get-bc src/redis-benchmark
