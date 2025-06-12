/// Adds two integers.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Subtracts b from a.
pub fn sub(a: i32, b: i32) -> i32 {
    a - b
}

/// Multiplies two integers.
pub fn mul(a: i32, b: i32) -> i32 {
    a * b
}

/// Divides a by b, returning `None` on divide-by-zero.
pub fn div(a: i32, b: i32) -> Option<i32> {
    if b == 0 {
        None
    } else {
        Some(a / b)
    }
}

/// Fancy addition behind a feature flag.
#[cfg(feature = "fancy")]
pub fn fancy_add(a: i32, b: i32) -> String {
    format!("✨ {} + {} = {} ✨", a, b, add(a, b))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basic_arithmetic() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(sub(7, 4), 3);
        assert_eq!(mul(6, 7), 42);
        assert_eq!(div(8, 2), Some(4));
        assert_eq!(div(1, 0), None);
    }

    #[test]
    #[cfg(feature = "fancy")]
    fn fancy_output() {
        let s = fancy_add(3, 4);
        assert!(s.contains("3 + 4 = 7"));
    }
}
