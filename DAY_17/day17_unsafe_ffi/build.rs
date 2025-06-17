fn main() {
    println!("cargo:rustc-link-search=native=../c_lib"); // Path to .so
    println!("cargo:rustc-link-lib=dylib=adder"); // Link libadder.so
}
