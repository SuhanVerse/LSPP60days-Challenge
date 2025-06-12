use calclib::{add, div, mul};

fn main() {
    println!("2 * 3 = {}", mul(2, 3));
    match div(10, 0) {
        Some(r) => println!("10 / 0 = {}", r),
        None => println!("Cannot divide by zero"),
    }
}
