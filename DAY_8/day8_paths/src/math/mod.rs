// Relative import of internal helper
use super::internal::math_only;

// Re-export operations at math module root
pub mod operations;
pub use operations::{add, multiply};

/// Calls the `math_only` helper
pub fn run_math_helper() {
    println!("[math] calling math_only");
    math_only();
}
