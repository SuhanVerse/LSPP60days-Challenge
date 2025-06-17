// Demonstrates reading and writing via raw pointers.
pub fn raw_pointer_demo() {
    let mut x = 42;
    let p: *mut i32 = &mut x;
    let q: *const i32 = &x;

    unsafe {
        // Dereference raw pointers
        *p += 1;
        println!("*p after +=1 = {}", *p);
        println!("*q = {}", *q);
    }

    println!("x = {}", x);
}

/// Computes the length of a C-style string (null-terminated).
/// 
/// # Safety
/// The caller must ensure that:
/// * The pointer is properly aligned and points to a valid memory location
/// * The string is null-terminated
/// * The memory remains valid for the duration of this function call
pub unsafe fn strlen(cstr: *const u8) -> usize {
    let mut len = 0;
    let mut ptr = cstr;

    unsafe {
        while *ptr != 0 {
            ptr = ptr.add(1);
            len += 1;
        }
    }
    len
}
