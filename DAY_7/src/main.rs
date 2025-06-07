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

// use std::fs::File;
// use std::io::{self, Read};

// fn read_username_from_file() -> Result<String, io::Error> {
//     let mut f = File::open("hello.txt")?;        // `?` propagates Err
//     let mut s = String::new();
//     f.read_to_string(&mut s)?;                   // propagates Err
//     Ok(s)                                        // return Ok on success
// }

// fn main() {
//     match read_username_from_file() {
//         Ok(name) => println!("Username: {}", name),
//         Err(e)   => eprintln!("Error reading file: {}", e),
//     }
// }

//------------------------------------------------------------------------------

// fn main() {
//     // unwrap_or: return default on Err
//     let v: Result<i32, &str> = Err("oops");
//     println!("{}", v.unwrap_or(42)); // prints 42

//     // unwrap: panic on Err
//     // let x = v.unwrap(); // panic!("called `Result::unwrap()` on an `Err` value")

//     // expect: panic with custom message
//     // v.expect("Failed to get value");

//     // map: transform success value
//     let pilot_id: Result<u32, &str> = Ok(7);
//     let doubled = pilot_id.map(|id| id * 2);
//     println!("{:?}", doubled); // Ok(14)
// }

//------------------------------------------------------------------------------

// /// Divides two numbers, returns Err if divisor is zero
// pub fn divide(dividend: i32, divisor: i32) -> Result<i32, String> {
//     if divisor == 0 {
//         Err(String::from("Cannot divide by zero"))
//     } else {
//         Ok(dividend / divisor)
//     }
// }

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_divide_success() {
//         assert_eq!(divide(10, 2).unwrap(), 5);
//     }

//     #[test]
//     #[should_panic(expected = "Cannot divide by zero")]
//     fn test_divide_zero() {
//         // unwrap() on Err triggers panic with our error message
//         divide(5, 0).unwrap();
//     }

//     #[test]
//     fn test_divide_error() {
//         let err = divide(5, 0).unwrap_err();
//         assert_eq!(err, "Cannot divide by zero");
//     }
// }

// ------------------------------------------------------------------------------


use DAY_7::{divide, ensure_positive, read_data}; // import functions from lib.rs

fn main() {
    match read_data() {
        Ok(text) => println!("Read data: {}", text),
        Err(e) => eprintln!("Error: {}", e),
    }

    match divide(10, 0) {
        Ok(v) => println!("10/2 = {}", v),
        Err(msg) => println!("Divide error: {}", msg),
    }

    ensure_positive(5);
    // ensure_positive(-1); // will panic
}
