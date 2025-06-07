// Declare the operations submodule (from operations.rs)
pub mod operations;

// Re-export commonly used functions at module root:
pub use operations::{add, multiply};
