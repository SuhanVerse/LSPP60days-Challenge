use DAY_13::{create_tuple, log, say_hello, vec_of_strings};

fn main() {
    // 1. Greeting
    say_hello!();

    // 2. Dynamic tuple struct
    create_tuple!(Calculator, f64);
    let calc = Calculator(3.0, 4.0);
    println!("Calculator sum: {}", calc.0 + calc.1);

    // 3. Build and display vector
    let languages = vec_of_strings!("Rust", "Go", "Python");
    println!("Languages: {:?}", languages);

    // 4. Logging
    log!("Application started");
    log!(INFO, "All systems go");
    log!(WARN, "This is a warning");
    log!(ERROR, "This is an error");
}
