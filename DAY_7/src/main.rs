// fn main() {
//     let v = vec![1, 2, 3];
//     println!("Element: {}", v[99]); // panics: index out of bounds
// }


//------------------------------------------------------------------------------


// fn fizzbuzz(n: i32) {
//     if n < 1 {
//         panic!("Input must be positive, got {}", n);
//     }
//     // ...
// }

// fn main() {
//     fizzbuzz(0); // will panic with your message
// }


//------------------------------------------------------------------------------


use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;        // `?` propagates Err
    let mut s = String::new();
    f.read_to_string(&mut s)?;                   // propagates Err
    Ok(s)                                        // return Ok on success
}

fn main() {
    match read_username_from_file() {
        Ok(name) => println!("Username: {}", name),
        Err(e)   => eprintln!("Error reading file: {}", e),
    }
}
