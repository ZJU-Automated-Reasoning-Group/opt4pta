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

SVF_HOME=~/SVF-dev

if [ -z "$WPA" ]; then
    echo "WARNING!!! envvar WPA is not set. Setting it to RBM"
    WPA="$SVF_HOME/Release-build-RBM/bin/wpa"
fi

echo "WPA: $WPA"

cp $bitcode_file $output_dir/

# (/usr/bin/time -v perf stat -- "$SVF_BV/wpa" -fspta $bitcode_file) && perf script > out.perf && ./FlameGraph/stackcollapse-perf.pl out.perf > out.folded && ./FlameGraph/flamegraph.pl out.folded > flamegraph.svg

# task_name="vfspta_all_opt_mutable"
# echo "Running $task_name"
# (/usr/bin/time -v "$WPA" -vfspta -opt-svfg=false -node-alloc-strat=dense -ptd=mutable -versioning-threads=16 -clock-type=wall $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"

task_name="ander_mutable"
echo "Running $task_name"
(/usr/bin/time -v "$WPA" -ander -ptd=mutable $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"


task_name="fspta_mutable_clustered"
echo "Running $task_name"
(/usr/bin/time -v "$WPA" -fspta -node-alloc-strat=dense -ptd=mutable $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"

# task_name="vfspta_all_opt_persistent"
# echo "Running $task_name"
# (/usr/bin/time -v "$WPA" -vfspta -opt-svfg=false -node-alloc-strat=dense -ptd=persistent -versioning-threads=16 -clock-type=wall $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"

# task_name="fspta_mutable"
# echo "Running $task_name"
# (/usr/bin/time -v "$WPA" -fspta -ptd=mutable $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"

# task_name="fspta_persistent"
# echo "Running $task_name"
# (/usr/bin/time -v "$WPA" -fspta -ptd=persistent $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"

task_name="fspta_persistent_clustered"
echo "Running $task_name"
(/usr/bin/time -v "$WPA" -fspta -node-alloc-strat=dense -ptd=persistent $bitcode_file > "$output_dir/$task_name$suffix.out") 2> "$output_dir/$task_name$suffix.timed.out"