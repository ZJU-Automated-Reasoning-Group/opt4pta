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

export SVF_HOME=~/SVF-dev
export SVF_SBV="$SVF_HOME/Release-build-RBM/bin"


ulimit -n 8192 # Idk but decrease it can make valgrind work
cp $bitcode_file $output_dir/

(/usr/bin/time -v perf record -F 99 -a -g --call-graph dwarf -o "$output_dir/RBM_$suffix.perf.data" -- "$SVF_SBV/wpa" -fspta -ptd=mutable -node-alloc-strat=dense -clock-type=wall $bitcode_file > "$output_dir/RBM_$suffix.out") 2> "$output_dir/RBM_$suffix.out"

# perf stat --all-user -etask-clock,context-switches,cpu-migrations,page-faults,cycles,instructions,uops_issued.any,uops_executed.thread


# perf script -i *clustered.perf.data > out_clustered.perf && stackcollapse-perf.pl out_clustered.perf > out_clustered.folded && flamegraph.pl out_clustered.folded > flamegraph.svg
