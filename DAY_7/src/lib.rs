use std::fs::File;
use std::io::{self, Read};

/// Reads the entire contents of `data.txt` and returns it as a `String`.
///
/// # Errors
/// Returns an `io::Error` if the file can't be opened or read.
pub fn read_data() -> Result<String, io::Error> {
    let mut file = File::open("data.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

/// Divides two integers, returning an error if the divisor is zero.
///
/// # Errors
/// Returns `Err` with a message if dividing by zero.
pub fn divide(dividend: i32, divisor: i32) -> Result<i32, String> {
    if divisor == 0 {
        Err("Cannot divide by zero".to_string())
    } else {
        Ok(dividend / divisor)
    }
}

/// Panics if the number is negative.
///
/// # Panics
/// Panics with a message if `n` is less than zero.
pub fn ensure_positive(n: i32) {
    if n < 0 {
        panic!("Negative input not allowed: {}", n);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_divide_ok() {
        assert_eq!(divide(10, 2).unwrap(), 5);
    }

    #[test]
    fn test_divide_err() {
        let error = divide(10, 0).unwrap_err();
        assert_eq!(error, "Cannot divide by zero");
    }

    #[test]
    #[should_panic(expected = "Negative input not allowed")]
    fn test_ensure_positive_panic() {
        ensure_positive(-1);
    }

    #[test]
    fn test_read_data_error() {
        let result = read_data();
        assert!(result.is_err(), "Expected an error for missing file");
    }

    // You can add another test for success case if data.txt is set up properly.
}
