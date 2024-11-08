perf script -i SBV_fspta_timed_0.perf.data > out.perf
stackcollapse-perf.pl out.perf > out.folded
flamegraph.pl out.folded > flamegraph.svg