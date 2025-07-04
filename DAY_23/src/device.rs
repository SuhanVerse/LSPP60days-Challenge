#![no_std]
#![cfg_attr(feature = "device", no_main)]

#[cfg(feature = "device")]
use cortex_m_rt::entry;

#[cfg(feature = "device")]
#[entry]
fn main() -> ! {
    // embedded blink demo…
}

// Put any host‐testable code here:
pub fn add(a: u32, b: u32) -> u32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
