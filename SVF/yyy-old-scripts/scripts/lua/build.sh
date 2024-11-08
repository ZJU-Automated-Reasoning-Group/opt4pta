make clean
rm ./*.bc

CC=gclang CXX=gclang++ ./all && echo "Make finished"

get-bc lua