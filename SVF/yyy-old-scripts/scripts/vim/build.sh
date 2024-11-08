make clean

# export LLVM_COMPILER=clang
export CC=gclang
export CXX=gclang++

(./configure && make -j) && echo "Make finished."

get-bc ./src/vim