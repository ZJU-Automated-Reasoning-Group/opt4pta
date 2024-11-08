export LLVM_COMPILER=clang

# make clean

export CC=gclang
export CXX=gclang++

./autogen.sh

(./configure && make -j) && echo "Make finished."

# make test

get-bc tmux
