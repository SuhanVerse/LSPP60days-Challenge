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
        let temp = math::absolute(a);
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

pub fn absolute(a: u32) -> u32 {
    if a < 0 {
        -a as u32 // Convert to positive
    } else {
        a // Already positive
    }
}
pub fn factorial(a: u32) -> u32 {
    if a == 0 || a == 1 {
        return 1; // Factorial of 0 and 1 is 1
    }
    let mut result = 1;
    for i in 2..=a {
        result *= i;
    }
    result
}
