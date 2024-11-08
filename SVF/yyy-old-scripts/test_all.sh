SVF_HOME=~/SVF-dev

# echo "Running: EWAH"
# export WPA="$SVF_HOME/Release-build-EWAH/bin/wpa"
# python test.py EWAH_benchmark_outputs test-utils/bitvec_benchmark.sh

# echo "Running: SBV-128-NOCUR"
# export WPA="$SVF_HOME/Release-build-SBV-NoOpt/bin/wpa"
# python test.py SBV-128-NOCUR_benchmark_outputs test-utils/bitvec_benchmark.sh

echo "Running: SBV-128OPT"
export WPA="$SVF_HOME/Release-build-SBV-128OPT/bin/wpa"
python test.py SBV-128OPT_benchmark_outputs test-utils/bitvec_benchmark.sh

echo "Running: RBM-Opt"
export WPA="$SVF_HOME/Release-build-RBM-OPT/bin/wpa"
python test.py RBM-OPT_benchmark_outputs test-utils/bitvec_benchmark.sh

echo "Running: RBM+COW+Bulk"
export WPA="$SVF_HOME/Release-build-RBM-cow-bulk/bin/wpa"
python test.py RBM-COW-BULK_benchmark_outputs test-utils/bitvec_benchmark.sh

echo "Running: SBV128"
export WPA="$SVF_HOME/Release-build-SBV-128/bin/wpa"
python test.py SBV128_benchmark_outputs test-utils/bitvec_benchmark.sh
