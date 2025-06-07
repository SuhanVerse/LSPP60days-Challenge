// #![allow(unused)]
// mod greetings {
//     pub fn hello() {
//         println!("Hello from greetings!");
//     }

//     mod secrets {
//         pub fn whisper() {
//             println!("This is a secret.");
//         }
//     }
// }

// fn main() {
//     greetings::hello();
//     // greetings::secrets::whisper(); // error: `secrets` is private
// }

//-----------------------------------------------------------------------

// src/main.rs

// Import the public API from your library crate
use DAY_8::{math, utils};

fn main() {
    // Call greet from utils.rs
    utils::greet("Rustacean");

    // Call add & multiply from math/operations.rs
    let sum = math::add(5, 7);
    let product = math::multiply(3, 4);

    println!("5 + 7 = {}", sum);
    println!("3 * 4 = {}", product);
}


//--------------------------------------------------------------------

