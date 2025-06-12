//! xrust_calclib: A simple floating‐point calculator library.

/// Adds two floating‐point numbers.
pub fn add(a: f64, b: f64) -> f64 {
    a + b
}

/// Subtracts `b` from `a`.
pub fn sub(a: f64, b: f64) -> f64 {
    a - b
}

/// Multiplies two floating‐point numbers.
pub fn mul(a: f64, b: f64) -> f64 {
    a * b
}

/// Divides `a` by `b`, returning an error if `b` is zero.
pub fn div(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero is not allowed".into())
    } else {
        Ok(a / b)
    }
}

/// Computes `a % b`, returning an error if `b` is zero.
pub fn mode(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Modulo by zero is not allowed".into())
    } else {
        Ok(a % b)
    }
}

/// Raises `a` to the power of `b`.
pub fn pow(a: f64, b: f64) -> f64 {
    a.powf(b)
}

/// Computes the square root of `a`, or errors if `a` is negative.
pub fn sqrt(a: f64) -> Result<f64, String> {
    if a < 0.0 {
        Err("Cannot calculate square root of a negative number".into())
    } else {
        Ok(a.sqrt())
    }
}

/// Returns the absolute value of `a`.
pub fn abs(a: f64) -> f64 {
    a.abs()
}

/// Computes the factorial of `a`. Only defined for non‐negative integers.
pub fn fact(a: f64) -> Result<f64, String> {
    if a < 0.0 {
        return Err("Cannot calculate factorial of a negative number".into());
    }
    if a.fract() != 0.0 {
        return Err("Factorial is not defined for non-integer values".into());
    }

    let mut result = 1.0;
    let mut n = a as u64;
    while n > 1 {
        result *= n as f64;
        n -= 1;
    }
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_sub_mul() {
        assert_eq!(add(2.5, 3.0), 5.5);
        assert_eq!(sub(7.0, 2.3), 4.7);
        assert_eq!(mul(4.0, 2.5), 10.0);
    }

    #[test]
    fn test_div() {
        assert_eq!(div(8.0, 2.0), Ok(4.0));
        assert_eq!(div(1.0, 0.0), Err("Division by zero is not allowed".into()));
    }

    #[test]
    fn test_mode() {
        assert_eq!(mode(10.5, 3.0), Ok(1.5));
        assert_eq!(mode(5.0, 0.0), Err("Modulo by zero is not allowed".into()));
    }

    #[test]
    fn test_pow_sqrt_abs() {
        assert_eq!(pow(2.0, 3.0), 8.0);
        assert_eq!(sqrt(9.0), Ok(3.0));
        assert_eq!(
            sqrt(-1.0),
            Err("Cannot calculate square root of a negative number".into())
        );
        assert_eq!(abs(-5.5), 5.5);
    }

    #[test]
    fn test_fact() {
        assert_eq!(fact(5.0), Ok(120.0));
        assert_eq!(fact(0.0), Ok(1.0));
        assert_eq!(
            fact(-3.0),
            Err("Cannot calculate factorial of a negative number".into())
        );
        assert_eq!(
            fact(3.5),
            Err("Factorial is not defined for non-integer values".into())
        );
    }
}
