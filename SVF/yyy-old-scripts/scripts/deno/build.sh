# rustup component add rust-src --toolchain nightly-2023-06-01-x86_64-unknown-linux-gnu
(RUSTFLAGS="--emit=llvm-bc" cargo build --release -Z build-std --target x86_64-unknown-linux-gnu) && echo "Cargo build finished."
# llvm-link --only-needed target/x86_64-unknown-linux-gnu/release/deps/deno-*.bc target/x86_64-unknown-linux-gnu/release/deps/*.bc > withalldeps.bc