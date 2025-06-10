// src/lib.rs

#![allow(non_snake_case)]
// Export the `utils` and `math` modules so they’re visible from the crate root
pub mod math;
pub mod utils;

// Re-export utils::greet so users of this library can call `day8_project::greet`
pub use utils::greet;
