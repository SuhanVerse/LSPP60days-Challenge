// #[allow(non_snake_case)]
// // fn main() {
// //     DAY_17::raw_pointer_demo();
// // }

// fn main() {
//     let s = std::ffi::CString::new("hello").unwrap();
//     let ptr = s.as_ptr();
//     let len = unsafe { DAY_17::strlen(ptr as *const u8) };
//     println!("Length = {}", len);
// }

fn main() {
    let sum = day17_unsafe_ffi::safe_add(5, 7);
    println!("5 + 7 = {}", sum);
}
