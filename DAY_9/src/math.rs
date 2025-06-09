pub fn add(a: f64, b: f64) -> f64 {
    a + b
}

pub fn sub(a: f64, b: f64) -> f64 {
    a - b
}

pub fn mul(a: f64, b: f64) -> f64 {
    a * b
}

pub fn div(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero is not allowed".to_string())
    } else {
        Ok(a / b)
    }
}

pub fn mode(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Modulo by zero is not allowed".to_string())
    } else {
        Ok(a % b)
    }
}

pub fn pow(a: f64, b: f64) -> f64 {
    a.powf(b)
}

pub fn sqrt(a: f64) -> Result<f64, String> {
    if a < 0.0 {
        Err("Cannot calculate square root of a negative number".to_string())
    } else {
        Ok(a.sqrt())
    }
}

pub fn abs(a: f64) -> f64 {
    a.abs()
}

pub fn fact(a: f64) -> Result<f64, String> {
    if a < 0.0 {
        return Err("Cannot calculate factorial of a negative number".to_string());
    }
    if a.fract() != 0.0 {
        return Err("Factorial is not defined for non-integer values".to_string());
    }

    let mut result = 1.0;
    let mut n = a as u64;
    while n > 1 {
        result *= n as f64;
        n -= 1;
    }
    Ok(result)
}
