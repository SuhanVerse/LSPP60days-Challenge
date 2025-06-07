// Absolute path import from crate root
use crate::internal::crate_helper;

/// A public utility function
pub fn greet(name: &str) {
    println!("Hello, {}!", name);
    crate_helper();
}

/// Returns the factorial of n (0! = 1)
pub fn factorial(n: u64) -> u64 {
    (1..=n).product()
}
