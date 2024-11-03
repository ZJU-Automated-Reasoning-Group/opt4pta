set -e

jobs=28

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SVFHOME="${SCRIPT_DIR}"
LLVMHome="llvm-14.0.0.obj"

# check if unzip is missing (Z3)
function check_unzip {
    if ! type unzip &> /dev/null; then
        echo "Cannot find unzip. Please install unzip."
        exit 1
    fi
}

function build_llvm_from_source {
    mkdir "$LLVMHome"
    check_unzip
    echo "Unzipping LLVM source..."
    mkdir llvm-14-source
    unzip llvmorg-14.0.0.zip -d llvm-14-source

    echo "Building LLVM..."
    mkdir llvm-14-build
    cd llvm-14-build
    # /*/ is a dirty hack to get llvm-project-llvmorg-version...
    cmake -G Ninja -DLIBCXX_ENABLE_SHARED=OFF -DLIBCXX_ENABLE_STATIC_ABI_LIBRARY=ON -DCMAKE_BUILD_TYPE=Release -DLLVM_BINUTILS_INCDIR=/opt/binutils/include -DCMAKE_INSTALL_PREFIX="$SVFHOME/$LLVMHome" -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld;lldb;compiler-rt;mlir;pstl;flang" ../llvm-14-source/*/llvm
    cmake --build . -j ${jobs}
    cmake --install .

    cd ..
    rm -r llvm-14-source llvm-14-build
}

build_llvm_from_source