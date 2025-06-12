/// Adds two numbers.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Subtracts two numbers.
pub fn subtract(a: i32, b: i32) -> i32 {
    a - b
}

/// Adds two numbers in a "fancy" way (prints and adds).
/// Enabled only if the `fancy` feature is enabled.
#[cfg(feature = "fancy")]
pub fn fancy_add(a: i32, b: i32) -> i32 {
    println!("✨ Fancy adding {} and {}!", a, b);
    a + b
}
