pub fn add(a: u32, b: u32) -> u32 {
    a + b
}
pub fn sub(a: u32, b: u32) -> u32 {
    a - b
}
pub fn mul(a: u32, b: u32) -> u32 {
    a * b
}
pub fn div(a: u32, b: u32) -> u32 {
    if b == 0 {
        error!("Division by zero is not allowed");
        0 // Return 0 or handle the error as needed
    }
    a / b
}
pub fn mode(a: u32, b: u32) -> u32 {
    if b == 0 {
        error!("Modulo by zero is not allowed");
        0 // Return 0 or handle the error as needed
    }
    a % b
}
pub fn pow(a: u32, b: u32) -> u32 {
    if b == 0 {
        return 1; // Any number to the power of 0 is 1
    }
    let mut result = 1;
    for _ in 0..b {
        result *= a;
    }
    result
}
pub fn sqrt(a: u32) -> u32 {
    if a == 0 {
        return 0; // The square root of 0 is 0
    }
    if a == 1 {
        return 1; // The square root of 1 is 1
    }
    if a < 0 {
        let temp = math::abs(a);
        let mut result = 0;
        let mut i = 1;
        while i * i <= temp {
            result = i;
            i += 1;
        }
        println!("THe SQUARE ROOT OF {} IS {}", a, result);
    } else {
        let mut result = 0;
        let mut i = 1;
        while i * i <= a {
            result = i;
            i += 1;
        }
        result
    }
}

pub fn abs(a: u32) -> u32 {
    if a < 0 {
        -a as u32 // Convert to positive
    } else {
        a // Already positive
    }
}
pub fn fact(a: u32) -> u32 {
    if a == 0 || a == 1 {
        return 1; // Factorial of 0 and 1 is 1
    }
    let mut result = 1;
    for i in 2..=a {
        result *= i;
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2.0, 3.0), 5.0);
    }

    #[test]
    fn test_sub() {
        assert_eq!(sub(5.0, 3.0), 2.0);
    }

    #[test]
    fn test_mul() {
        assert_eq!(mul(2.0, 4.0), 8.0);
    }

    #[test]
    fn test_div_ok() {
        assert_eq!(div(10.0, 2.0).unwrap(), 5.0);
    }

    #[test]
    fn test_div_err() {
        assert!(div(1.0, 0.0).is_err());
    }

    #[test]
    fn test_mode_ok() {
        assert_eq!(mode(10.0, 3.0).unwrap(), 1.0);
    }

    #[test]
    fn test_mode_err() {
        assert!(mode(10.0, 0.0).is_err());
    }

    #[test]
    fn test_factorial() {
        assert_eq!(fact(5.0).unwrap(), 120.0);
        assert_eq!(fact(0.0).unwrap(), 1.0);
        assert_eq!(fact(1.0).unwrap(), 1.0);
    }

    #[test]
    fn test_factorial_err() {
        assert!(fact(-5.0).is_err());
    }

    #[test]
    fn test_sqrt() {
        assert_eq!(sqrt(4.0).unwrap(), 2.0);
        assert_eq!(sqrt(0.0).unwrap(), 0.0);
        assert_eq!(sqrt(1.0).unwrap(), 1.0);
        assert!(sqrt(-4.0).is_err());
    }

    #[test]
    fn test_abs() {
        assert_eq!(abs(5.0).unwrap(), 5.0);
        assert_eq!(abs(-5.0).unwrap(), 5.0);
        assert_eq!(abs(0.0).unwrap(), 0.0);
    }

    #[test]
    fn test_pow() {
        assert_eq!(pow(2.0, 3.0).unwrap(), 8.0);
        assert_eq!(pow(5.0, 0.0).unwrap(), 1.0);
        assert_eq!(pow(3.0, 2.0).unwrap(), 9.0);
    }

    #[test]
    fn test_pow_err() {
        assert!(pow(2.0, -1.0).is_err());
    }
}
