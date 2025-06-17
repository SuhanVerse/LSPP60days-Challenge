unsafe extern "C" {
    fn add(a: i32, b: i32) -> i32;
}

/// Safe wrapper around the unsafe C function
pub fn safe_add(a: i32, b: i32) -> i32 {
    unsafe { add(a, b) }
}
