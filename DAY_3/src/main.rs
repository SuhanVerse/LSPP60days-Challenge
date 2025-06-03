// fn main() {
//     let a = 42;
//     let b = 1;
//     let c = do_sum(a, b);
//     println!("The sum of {} and {} is {}", a, b, c);
// }

// fn do_sum(a: i32, b: i32) -> i32 { // -> indicates the return type
//     a + b // no semicolon here, as this is the return value of the function
// }

//----------------------------------------------------------------------------------

// fn main() {
//     let a =  String::from("ISPP03");
//     println!("The value of a is: {}", a);
//     let b = a;
//     // println!("The value of a is: {}", a); // This will cause a compile-time error because `a` has been moved to `b`
//     println!("The value of b is: {}", b); // This will work because `b` now owns the value
// }

// ----------------------------------------------------------------------------------

// fn main() {
//     let t1= String::from("Hello, ");
//     let t2 = String::from("RUST!");
//     let t3 = do_concat(t1, t2);
//     println!("{}", t3);
//     }

// fn do_concat(s1: String, s2: String) -> String {

//     s1 + &s2 // `s1` is moved here and `s2` is borrowed
//     // no semicolon, this is the return value
// }
// Note: In Rust, when you use the `+` operator with a `String`, the first operand is moved and the second operand is borrowed.
// This means that `s1` is no longer valid after the operation, but `s2` can still be used because it was borrowed with `&`.

// -----------------------------------------------------------------------------------

// fn main() {
//     let str_1 = String::from("OWNERSHIP");
//     // takes_ownership(str_1);
//     let st_3 = takes_ownership(str_1);
//     //st_3 = takes_ownership(str_1.clone()); // This would work if you want to keep str_1 valid
//     println!("{}", st_3); // This will cause a compile-time error because str_1 has been moved
// }

// fn takes_ownership(some_string: String) -> String {
//     println!("{}", some_string);
//     some_string // This is the return value, which is moved back to the caller
// }

// -----------------------------------------------------------------------------------
// fn main() {
//     let my_string = String::from("Hello, Rust!");
//     takes_ownership(&my_string);  // Pass a reference to my_string
//     println!("{}", my_string);    // This is valid because ownership was not transferred
// }

// fn takes_ownership(some_string: &String) {
//     println!("{}", some_string);  // some_string is borrowed and not moved
// }

// -----------------------------------------------------------------------------------


// fn main() {
//     let mut s1 = String::from("Hello");
//     update_word(&mut s1);
//     println!("{}", s1);
// }

// fn update_word(word: &mut String) {
//     word.push_str(" World");
// }

// -----------------------------------------------------------------------------------

fn main() {
    let mut s1 = String::from("Hello");
    let s2 = &mut s1;
    s2.push_str(" World");
    println!("{}", s2); // This will print "Hello World"
}


