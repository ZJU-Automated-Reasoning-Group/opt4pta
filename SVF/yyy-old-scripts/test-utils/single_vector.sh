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

export SVF_HOME=~/SVF
export SVF_SBV="$SVF_HOME/RelWithDebInfo-build-SBV/bin"
export SVF_CBV="$SVF_HOME/RelWithDebInfo-build-CBV/bin"
export SVF_BV="$SVF_HOME/RelWithDebInfo-build-BV/bin"


ulimit -n 8192 # Idk but decrease it can make valgrind work
cp $bitcode_file $output_dir/

# (/usr/bin/time -v perf stat -- "$SVF_BV/wpa" -fspta $bitcode_file) && perf script > out.perf && ./FlameGraph/stackcollapse-perf.pl out.perf > out.folded && ./FlameGraph/flamegraph.pl out.folded > flamegraph.svg

(/usr/bin/time -v perf record -F 99 -a -g --call-graph dwarf -o "$output_dir/SBV$suffix.perf.data" -- "$SVF_SBV/wpa" -fspta $bitcode_file) 2> "$output_dir/SBV_timed$suffix.out"
(/usr/bin/time -v perf record -F 99 -a -g --call-graph dwarf -o "$output_dir/BV$suffix.perf.data" -- "$SVF_BV/wpa" -fspta $bitcode_file) 2> "$output_dir/BV_timed$suffix.out"
(/usr/bin/time -v perf record -F 99 -a -g --call-graph dwarf -o "$output_dir/CBV$suffix.perf.data" -- "$SVF_CBV/wpa" -fspta $bitcode_file) 2> "$output_dir/CBV_timed$suffix.out"

# (/usr/bin/time -v perf stat -o "$output_dir/SBV$suffix.stat.txt" -- "$SVF_SBV/wpa" -fspta $bitcode_file) 2> "$output_dir/SBV_timed$suffix.out"
# (/usr/bin/time -v perf stat -o "$output_dir/BV$suffix.stat.txt" -- "$SVF_BV/wpa" -fspta $bitcode_file) 2> "$output_dir/BV_timed$suffix.out"
# (/usr/bin/time -v perf stat -o "$output_dir/CBV$suffix.stat.txt" -- "$SVF_CBV/wpa" -fspta $bitcode_file) 2> "$output_dir/CBV_timed$suffix.out"

# perf stat --all-user -etask-clock,context-switches,cpu-migrations,page-faults,cycles,instructions,uops_issued.any,uops_executed.thread


# && perf script > out.perf && ./FlameGraph/stackcollapse-perf.pl out.perf > out.folded && ./FlameGraph/flamegraph.pl out.folded > flamegraph.svg
