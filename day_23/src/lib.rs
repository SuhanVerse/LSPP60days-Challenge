// When building with `--features device`, we compile as no_std.
// Otherwise we get std/test on the host.
#![cfg_attr(feature = "device", no_std)]

// Put all routines you want to test here.
pub fn add(a: u32, b: u32) -> u32 {
    a + b
}

// Only compiled in host tests.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
