use xrust_calclib::{abs, add, div, fact, mode, mul, pow, sqrt, sub};

fn main() {
    println!("3.5 + 2.1 = {}", add(3.5, 2.1));
    println!("7.0 - 5.5 = {}", sub(7.0, 5.5));
    println!("4.0 * 2.5 = {}", mul(4.0, 2.5));

    match div(10.0, 2.0) {
        Ok(result) => println!("10 / 2 = {}", result),
        Err(e) => println!("Error dividing: {}", e),
    }
    match div(10.0, 0.0) {
        Ok(result) => println!("10 / 0 = {}", result),
        Err(e) => println!("Error dividing: {}", e),
    }

    match mode(10.5, 3.0) {
        Ok(result) => println!("10.5 % 3 = {}", result),
        Err(e) => println!("Error modulo: {}", e),
    }

    println!("2^8 = {}", pow(2.0, 8.0));
    match sqrt(9.0) {
        Ok(r) => println!("√9 = {}", r),
        Err(e) => println!("Error sqrt: {}", e),
    }
    println!("|-5.5| = {}", abs(-5.5));

    match fact(5.0) {
        Ok(r) => println!("5! = {}", r),
        Err(e) => println!("Error factorial: {}", e),
    }
    match fact(-3.0) {
        Ok(r) => println!("-3! = {}", r),
        Err(e) => println!("Error factorial: {}", e),
    }
}
