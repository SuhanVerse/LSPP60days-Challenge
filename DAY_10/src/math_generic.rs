// // src/math_generic.rs

// use std::ops::{Add, Div, Mul, Sub};

// pub fn operate<T>(op: &str, a: T, b: T) -> Result<T, String>
// where
//     T: Copy
//         + Add<Output = T>
//         + Sub<Output = T>
//         + Mul<Output = T>
//         + Div<Output = T>
//         + PartialEq
//         + From<u8>,
// {
//     match op {
//         "add" => Ok(a + b),
//         "sub" => Ok(a - b),
//         "mul" => Ok(a * b),
//         "div" => {
//             if b == T::from(0) {
//                 Err("Cannot divide by zero".into())
//             } else {
//                 Ok(a / b)
//             }
//         }
//         _ => Err(format!("Unsupported operation: {}", op)),
//     }
// }


//-------------------------------------------------------------------

// src/math_generic.rs

use std::ops::{Add, Sub, Mul, Div};

pub fn operate<T>(op: &str, a: T, b: T) -> Result<T, String>
where
    T: Copy
        + Add<Output = T>
        + Sub<Output = T>
        + Mul<Output = T>
        + Div<Output = T>
        + PartialEq
        + From<u8>,
{
    match op {
        "add" => Ok(a + b),
        "sub" => Ok(a - b),
        "mul" => Ok(a * b),
        "div" => {
            if b == T::from(0) {
                Err("Cannot divide by zero".into())
            } else {
                Ok(a / b)
            }
        }
        _ => Err(format!("Unsupported operation: {}", op)),
    }
}
