use day17_unsafe_ffi::safe_add;

fn main() {
    let result = safe_add(5, 7);
    println!("5 + 7 = {}", result);
}
