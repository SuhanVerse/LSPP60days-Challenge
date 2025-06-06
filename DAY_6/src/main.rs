// fn main() {
//     // 1. Creating a Vector
//     let mut v: Vec<i32> = Vec::new();
//     let v2 = vec![1, 2, 3];

//     println!("Initial empty vector: {:?}", v);
//     println!("Vector with initial values: {:?}", v2);

//     // 2. Pushing and Popping Elements
//     v.push(10);
//     v.push(20);
//     v.push(30);
//     println!("After pushes: {:?}", v); // [10, 20, 30]

//     if let Some(last) = v.pop() {
//         println!("Popped: {}", last); // 30
//     }
//     println!("After pop: {:?}", v); // [10, 20]

//     // 3. Accessing and Iterating
//     let v3 = vec![100, 200, 300, 300, 400, 200];
//     // Direct indexing (panics if out of bounds)
//     println!("v3[1] = {}", v3[1]); // 200

//     // Using get() returns Option<&T>
//     match v3.get(5) {
//         Some(val) => println!("Found: {}", val),
//         None => println!("No element at index 5"),
//     }

//     // Immutable iteration
//     for val in &v3 {
//         println!("Got (immutable): {}", val);
//     }

//     // Mutable iteration: modify each element
//     let mut v4 = vec![1, 2, 3];
//     for x in &mut v4 {
//         *x += 10; // dereference to change the value
//     }
//     println!("Modified (after mutable iteration): {:?}", v4); // [11, 12, 13]
// }

//--------------------------------------------------------------------------------------

#![allow(unused_variables)]
fn main() {
    // 1. &str: String Slices
    let greeting: &str = "hello, world";
    println!("String slice (immutable): {}", greeting);

    // 2. String: Heap-Allocated, Growable String
    let s = String::new();
    println!("Empty String: '{}'", s);

    let mut s2 = String::from("hello");
    s2.push('!');
    s2.push_str(" world");
    println!("Modified String: {}", s2); // "hello! world"

    // 3. Common String Operations
    let s3 = String::from("rustacean");
    println!("s3 = '{}', length = {}", s3, s3.len());
    // Concatenation using `+` (moves s4, borrows s5)
    let s4 = String::from("hello, ");
    let s5 = String::from("world!");
    let s6 = s4 + &s5; // s4 is moved; s5 is borrowed
    println!("Concatenated with +: {}", s6);

    // Using format! to avoid moving
    let s7 = format!("{}{}", "foo", "bar");
    println!("Formatted with format!: {}", s7);

    // Iterating over characters (UTF-8)
    for c in "नमस्ते".chars() {
        println!("char: {}", c);
    }

    // Iterating over bytes
    for b in "नमस्ते".bytes() {
        println!("byte: {}", b);
    }

    // Slicing must respect UTF-8 boundaries
    let hello = String::from("Здравствуйте");
    // The first two Cyrillic letters take 4 bytes total in UTF-8
    for c in hello.bytes() {
        println!("Bytes: {}", c);
    }
    let slice = &hello[0..4];
    println!("Slice of '{}' is '{}'", hello, slice);
}


//--------------------------------------------------------------------------------------


