#!/bin/bash
# echo "test:"$PWD > test.output

# Must specify output dir
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <output_directory> <bitcode_file> <log_suffix>"
    exit 1
fi

output_dir="$1"
bitcode_file="$2"
suffix="$3"

if [ ! -d "$output_dir" ]; then
    echo "Error: Output directory '$output_dir' does not exist or is not a directory."
    exit 1
fi

if [ ! -f "$bitcode_file" ]; then
    echo "Error: Bitcode file '$bitcode_file' is not provided."
    exit 1
fi

echo "Start testing"

### MAIN

ulimit -n 8192 # Idk but decrease it can make valgrind work
cp $bitcode_file $output_dir/
(/usr/bin/time -v valgrind --tool=massif --log-file="$output_dir/valgrind$suffix.log"\
 --massif-out-file="$output_dir/massif$suffix.out" wpa -fspta $bitcode_file > "$output_dir/wpa$suffix.out") 2> "$output_dir/timed$suffix.out"